# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/classes/50_DomoAccount.ipynb.

# %% auto 0
__all__ = ['Account_CanIModify', 'UpsertAccount_MatchCriteria', 'DomoAccount', 'DomoAccounConfig_MissingFields', 'DomoAccounts',
           'Account_Accesslist_Share', 'Account_Accesslist']

# %% ../../nbs/classes/50_DomoAccount.ipynb 3
from dataclasses import dataclass, field
from typing import Any, List

import datetime as dt
import re

import httpx

from nbdev.showdoc import patch_to

import domolibrary.utils.convert as cd
import domolibrary.utils.DictDot as util_dd
import domolibrary.client.DomoAuth as dmda
import domolibrary.client.DomoError as de
import domolibrary.routes.account as account_routes

import domolibrary.utils.chunk_execution as ce

# %% ../../nbs/classes/50_DomoAccount.ipynb 4
from domolibrary.routes.account import (
    ShareAccount_V1_AccessLevel,
    ShareAccount_V2_AccessLevel,
    ShareAccount,
    GetAccount_NoMatch,
    ShareAccount_Error,
    ShareAccount_Error_AlreadyShared,
    DeleteAccount_Error,
)

from domolibrary.classes.DomoAccount_Config import (
    AccountConfig_UsesOauth,
    AccountConfig_ProviderTypeNotDefined,
    DomoAccount_Config,
    AccountConfig,
)


class Account_CanIModify(de.DomoError):
    def __init__(self, account_id, domo_instance):
        super().__init__(
            message=f"`DomoAccount.is_admin_summary` must be `False` to proceed.  Either set the value explicity, or retrieve the account instance using `DomoAccount.get_by_id()`",
            domo_instance=domo_instance,
        )


class UpsertAccount_MatchCriteria(de.DomoError):
    def __init__(self, domo_instance):
        super().__init__(
            message="must pass an account_id or account_name to UPSERT",
            domo_instance=domo_instance,
        )

# %% ../../nbs/classes/50_DomoAccount.ipynb 6
@dataclass
class DomoAccount:
    id: int
    auth: dmda.DomoAuth = field(repr=False)

    name: str = None
    data_provider_type: str = None

    created_dt: dt.datetime = None
    modified_dt: dt.datetime = None

    config: DomoAccount_Config = None

    owner: List[Any] = None  # DomoUser or DomoGroup

    is_admin_summary: bool = True

    @classmethod
    def _from_json(
        cls,
        obj: dict,
        is_admin_summary: bool = True,
        auth: dmda.DomoAuth = None,
    ):
        """converts data_v1_accounts API response into an accounts class object"""

        dd = util_dd.DictDot(obj)

        return cls(
            id=dd.id or dd.databaseId,
            name=dd.displayName,
            data_provider_type=dd.dataProviderId or dd.dataProviderType,
            created_dt=cd.convert_epoch_millisecond_to_datetime(
                dd.createdAt or dd.createDate
            ),
            modified_dt=cd.convert_epoch_millisecond_to_datetime(
                dd.modifiedAt or dd.lastModified
            ),
            auth=auth,
            is_admin_summary=is_admin_summary,
        )

# %% ../../nbs/classes/50_DomoAccount.ipynb 8
class DomoAccounConfig_MissingFields(de.DomoError):
    def __init__(self, domo_instance, missing_keys, account_id):
        super().__init__(
            domo_instance=domo_instance,
            message=f"{account_id} config class definition is missing the following keys - {', '.join(keys)} extend the AccountConfig",
        )


@patch_to(DomoAccount)
def _test_missing_keys(self, res_obj, config_obj):
    return [r_key for r_key in res_obj.keys() if r_key not in config_obj.keys()]


@patch_to(DomoAccount)
async def _get_config(
    self: DomoAccount,
    session=None,
    return_raw: bool = False,
    debug_api: bool = None,
    auth: dmda.DomoAuth = None,
    debug_num_stacks_to_drop=2,
    is_suppress_no_config: bool = False,  # can be used to suppress cases where the config is not defined, either because the account_config is OAuth, and therefore not stored in Domo OR because the AccountConfig class doesn't cover the data_type
):
    if not self.data_provider_type:
        res = await account_routes.get_account_from_id(
            auth=self.auth,
            account_id=self.id,
            session=session,
            debug_api=debug_api,
            parent_class=self.__class__.__name__,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        self.data_provider_type = res.response["dataProviderType"]

    res = await account_routes.get_account_config(
        auth=auth or self.auth,
        account_id=self.id,
        session=session,
        debug_api=debug_api,
        data_provider_type=self.data_provider_type,
        parent_class=self.__class__.__name__,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    config_fn = AccountConfig(self.data_provider_type).value

    if not is_suppress_no_config and not config_fn.is_defined_config:
        raise config_fn._associated_exception(self.data_provider_type)

    self.config = config_fn._from_json(res.response)

    if self.config and self.config.to_json() != {}:
        if not res.response:
            print(self.data_provider_type, "no response")

        if not self.config.to_json():
            print(
                self.id,
                self.data_provider_type,
                "no config",
                self.config.to_json(),
                res.response,
            )

        self._test_missing_keys(res_obj=res.response, config_obj=self.config.to_json())

    return self.config

# %% ../../nbs/classes/50_DomoAccount.ipynb 11
@patch_to(DomoAccount, cls_method=True)
async def get_by_id(
    cls,
    auth: dmda.DomoAuth,
    account_id: int,
    is_suppress_no_config: bool = True,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    debug_api: bool = False,
    debug_num_stacks_to_drop=2,
):
    """retrieves account metadata and attempts to retrieve config"""

    res = await account_routes.get_account_from_id(
        auth=auth,
        account_id=account_id,
        session=session,
        debug_api=debug_api,
        parent_class=cls.__name__,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    acc = cls._from_json(obj=res.response, auth=auth, is_admin_summary=False)

    await acc._get_config(
        session=session,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        is_suppress_no_config=is_suppress_no_config,
    )

    return acc

# %% ../../nbs/classes/50_DomoAccount.ipynb 18
@patch_to(DomoAccount, cls_method=True)
async def create_account(
    cls: DomoAccount,
    account_name: str,
    config: DomoAccount_Config,
    auth: dmda.DomoAuth,
    debug_api: bool = False,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
):
    body = account_routes.generate_create_body(account_name=account_name, config=config)

    res = await account_routes.create_account(
        auth=auth, config_body=body, debug_api=debug_api, session=session
    )

    if return_raw:
        return res

    return await cls.get_by_id(auth=auth, account_id=res.response.get("id"))

# %% ../../nbs/classes/50_DomoAccount.ipynb 20
@patch_to(DomoAccount)
async def update_config(
    self: DomoAccount,
    auth: dmda.DomoAuth = None,
    debug_api: bool = False,
    config: DomoAccount_Config = None,
    is_suppress_no_config=False,
    debug_num_stacks_to_drop=2,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    auth = auth or self.auth
    config = config or self.config

    res = await account_routes.update_account_config(
        auth=auth,
        account_id=self.id,
        config_body=config.to_json(),
        debug_api=debug_api,
        session=session,
    )

    if return_raw:
        return res

    if not res.is_success and self.is_admin_summary:
        raise Account_CanIModify(account_id=self.id, domo_instance=auth.domo_instance)

    await self._get_config(
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        is_suppress_no_config=is_suppress_no_config,
    )

    return self

# %% ../../nbs/classes/50_DomoAccount.ipynb 25
@patch_to(DomoAccount)
async def update_name(
    self: DomoAccount,
    account_name: str = None,
    auth: dmda.DomoAuth = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    auth = auth or self.auth

    res = await account_routes.update_account_name(
        auth=auth,
        account_id=self.id,
        account_name=account_name or self.name,
        debug_api=debug_api,
        session=session,
    )

    if return_raw:
        return res

    if not res.is_success and self.is_admin_summary:
        raise Account_CanIModify(account_id=self.id, domo_instance=auth.domo_instance)

    await self.get_by_id(auth=auth, account_id=self.id)

    return self

# %% ../../nbs/classes/50_DomoAccount.ipynb 30
@patch_to(DomoAccount)
async def delete_account(
    self: DomoAccount,
    auth: dmda.DomoAuth = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=2,
    parent_class=None,
):
    auth = auth or self.auth

    res = await account_routes.delete_account(
        auth=auth,
        account_id=self.id,
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if not res.is_success and self.is_admin_summary:
        raise Account_CanIModify(account_id=self.id, domo_instance=auth.domo_instance)

    return res

# %% ../../nbs/classes/50_DomoAccount.ipynb 32
@patch_to(DomoAccount)
async def is_feature_accountsv2_enabled(
    self: DomoAccount, auth: dmda.DomoFullAuth = None, return_raw: bool = False
):
    """uses bootstrap class to test if the auth object refers to an instancce that has the account-v2 feature switch enabled"""
    import domolibrary.classes.DomoBootstrap as dmbs

    auth = auth or self.auth

    domo_bsr = dmbs.DomoBootstrap(auth=auth)

    try:
        is_v2 = await domo_bsr.is_feature_accountsv2_enabled()
        return 1 if is_v2 else 0

    except dmbs.InvalidAuthTypeError as e:
        print(
            f"Warning - unable to test if accounts_v2 feature is enabled in {auth.domo_instance}, recommend pass FullAuth"
        )
        return -1

# %% ../../nbs/classes/50_DomoAccount.ipynb 35
@patch_to(DomoAccount)
async def _share_v2(
    self: DomoAccount,
    auth: dmda.DomoAuth = None,
    user_id=None,
    group_id=None,
    access_level: ShareAccount = ShareAccount_V2_AccessLevel.CAN_VIEW,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=2,
    return_raw: bool = False,
    is_suppress_already_shared: bool = True,
):
    auth = auth or self.auth

    is_v2 = await self.is_feature_accountsv2_enabled(auth=auth)

    if is_v2 == 0:
        raise account_routes.ShareAccount_Error(
            account_id=self.id,
            response="accounts_v2 feature not enabled, use v1 share method",
            domo_instance=auth.domo_instance,
            function_name="_share_v2",
            parent_class=self.__class__.__name__,
            status=None,
        )

    share_payload = account_routes.generate_share_account_payload_v2(
        user_id=user_id,
        group_id=group_id,
        access_level=access_level,
    )
    try:
        res = await account_routes.share_account_v2(
            auth=auth,
            account_id=self.id,
            share_payload=share_payload,
            debug_api=debug_api,
            session=session,
            parent_class=self.__class__.__name__,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        return f"shared {self.id} - {self.name} with {group_id or user_id}"

    except ShareAccount_Error_AlreadyShared as e:
        if not is_suppress_already_shared:
            raise e

        return f"already shared {self.id} - {self.name} with {group_id or user_id}"

# %% ../../nbs/classes/50_DomoAccount.ipynb 38
@patch_to(DomoAccount)
async def _share_v1(
    self: DomoAccount,
    auth: dmda.DomoAuth = None,
    user_id=None,
    access_level: ShareAccount = ShareAccount_V1_AccessLevel.CAN_VIEW,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=2,
    return_raw: bool = False,
    is_suppress_already_shared: bool = True,
):
    auth = auth or self.auth

    is_v2 = await self.is_feature_accountsv2_enabled(auth=auth)

    if is_v2 == 1:
        raise account_routes.ShareAccount_Error(
            account_id=self.id,
            response="accounts_v2 feature enabled, use v2 share method",
            domo_instance=auth.domo_instance,
            function_name="_share_v2",
            parent_class=self.__class__.__name__,
            status=None,
        )

    share_payload = account_routes.generate_share_account_payload_v1(
        user_id=user_id,
        access_level=access_level,
    )
    try:
        res = await account_routes.share_account_v1(
            auth=auth,
            account_id=self.id,
            share_payload=share_payload,
            debug_api=debug_api,
            session=session,
            parent_class=self.__class__.__name__,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        return f"shared {self.id} - {self.name} with { user_id}"

    except ShareAccount_Error_AlreadyShared as e:
        if is_suppress_already_shared:
            return f"already shared {self.id} - {self.name} with { user_id}"

        else:
            raise e

# %% ../../nbs/classes/50_DomoAccount.ipynb 41
@patch_to(DomoAccount)
async def share(
    self: DomoAccount,
    user_id=None,
    group_id=None,
    domo_user=None,
    domo_group=None,
    auth: dmda.DomoAuth = None,
    access_level: ShareAccount = None,  # will default to Read
    is_suppress_already_shared: bool = True,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 3,
    debug_prn: bool = False,
    session: httpx.AsyncClient = None,
):
    auth = auth or self.auth
    is_v2 = await self.is_feature_accountsv2_enabled(auth=auth)

    user_id = user_id or (domo_user and domo_user.id)

    debug = {"is_accounts_v2": is_v2}

    res = None

    if is_v2 == 1:
        group_id = group_id or (domo_group and domo_group.id)

        debug.update(
            {
                "user_id*": user_id,
                "group_id": group_id,
            }
        )

        if debug_prn:
            print(debug)

        res = await self._share_v2(
            auth=auth,
            user_id=user_id,
            group_id=group_id,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            session=session,
            is_suppress_already_shared=is_suppress_already_shared,
        )

    elif is_v2 == 0:
        user_ids = [user_id]

        if group_id:
            import domolibrary.classes.DomoGroup as dmdg

            domo_group = await dmdg.DomoGroup.get_by_id(group_id=group_id, auth=auth)

        group_id = group_id or domo_group.id
        domo_users = await domo_group.Membership.get_members()
        user_ids = [domo_user.id for domo_user in domo_users]

        debug.update({"group_id": group_id, "user_ids": user_ids})

        if debug_prn:
            print(debug)

        res = await ce.gather_with_concurrency(
            *[
                self._share_v1(
                    auth=auth,
                    user_id=user_id,
                    debug_api=debug_api,
                    debug_num_stacks_to_drop=debug_num_stacks_to_drop,
                    session=session,
                    is_suppress_already_shared=is_suppress_already_shared,
                )
                for user_id in user_ids
            ],
            n=10,
        )

    return res

# %% ../../nbs/classes/50_DomoAccount.ipynb 45
@dataclass
class DomoAccounts:
    auth: dmda.DomoAuth

# %% ../../nbs/classes/50_DomoAccount.ipynb 46
@staticmethod
@patch_to(DomoAccounts)
async def _get_accounts_accountsapi(
    auth: dmda.DomoAuth,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    res = await account_routes.get_accounts(
        auth=auth, debug_api=debug_api, session=session
    )

    if return_raw:
        return res

    if len(res.response) == 0:
        return []

    return await ce.gather_with_concurrency(
        n=60,
        *[
            DomoAccount.get_by_id(
                account_id=json_obj.get("id"),
                debug_api=debug_api,
                session=session,
                auth=auth,
            )
            for json_obj in res.response
        ],
    )


@patch_to(DomoAccounts, cls_method=True)
async def _get_accounts_queryapi(
    cls: DomoAccounts,
    auth: dmda.DomoAuth,
    debug_api: bool = False,
    additional_filters_ls=None,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    """v2 api for works with group_account_v2 beta"""

    import domolibrary.routes.datacenter as datacenter_routes

    res = await datacenter_routes.search_datacenter(
        auth=auth,
        entity_type=datacenter_routes.Datacenter_Enum.ACCOUNT.value,
        additional_filters_ls=additional_filters_ls,
        session=session,
        debug_api=debug_api,
    )

    if return_raw:
        return res

    if len(res.response) == 0:
        return []

    return [
        DomoAccount._from_json(account_obj, auth=auth) for account_obj in res.response
    ]


@patch_to(DomoAccounts, cls_method=True)
async def get_accounts(
    cls: DomoAccounts,
    auth: dmda.DomoAuth,
    additional_filters_ls=None,  # datacenter_routes.generate_search_datacenter_filter
    # account string to search for, must be an exact match in spelling.  case insensitive
    # v2 will use the queryAPI as it returns more complete results than the accountsAPI
    is_v2: bool = None,
    is_suppress_undefined_provider_type: bool = False,
    account_name: str = None,
    account_id: str = None,
    account_type: AccountConfig = None,  # to retrieve a specific account type
    account_type_str=None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    debug_prn: bool = False,
):
    import domolibrary.classes.DomoBootstrap as bsr
    import domolibrary.routes.datacenter as datacenter_routes

    if isinstance(auth, dmda.DomoFullAuth) and is_v2 is None:
        instance_bsr = bsr.DomoBootstrap(auth=auth)

        is_v2 = await instance_bsr.is_feature_accountsv2_enabled(auth)

        if debug_prn:
            print(
                f"{auth.domo_instance} {'is' if is_v2 else 'is not'} using the v2 beta"
            )

    if is_v2:
        try:
            domo_accounts = await cls._get_accounts_queryapi(
                auth=auth,
                debug_api=debug_api,
                additional_filters_ls=additional_filters_ls,
                session=session,
            )
        except datacenter_routes.SearchDatacenter_NoResultsFound as e:
            print(e)
            domo_accounts = []
    else:
        domo_accounts = await cls._get_accounts_accountsapi(
            auth=auth, debug_api=debug_api, session=session
        )

    if return_raw or len(domo_accounts) == 0:
        return domo_accounts

    if account_id:
        domo_account = next(
            (
                domo_account
                for domo_account in domo_accounts
                if int(domo_account.id) == int(account_id)
            ),
            None,
        )

        if not domo_account:
            raise GetAccount_NoMatch(
                account_id=account_id, domo_instance=auth.domo_instance
            )

        return domo_account

    if account_name and isinstance(account_name, str):
        domo_accounts = [
            domo_account
            for domo_account in domo_accounts if domo_account.name.lower() == account_name.lower()
        ]

    if account_type:
        return [
            domo_account
            for domo_account in domo_accounts
            if domo_account.data_provider_type == account_type.value.data_provider_type
        ]

    if account_type_str:
        return [
            domo_account
            for domo_account in domo_accounts
            if domo_account.data_provider_type == account_type_str
        ]

    return domo_accounts

# %% ../../nbs/classes/50_DomoAccount.ipynb 49
@dataclass
class Account_Accesslist_Share:
    entity: Any
    access_level: ShareAccount
    auth: dmda.DomoAuth

    @staticmethod
    async def _get_entity(obj, auth: dmda.DomoAuth):
        if obj["type"] == "USER":
            import domolibrary.classes.DomoUser as dmu

            return await dmu.DomoUser.get_by_id(user_id=obj["id"], auth=auth)

        if obj["type"] == "GROUP":
            import domolibrary.classes.DomoGroup as dmg

            return await dmg.DomoGroup.get_by_id(group_id=obj["id"], auth=auth)

        return None

    @staticmethod
    def _get_access_level(access_level, is_v2: int):
        if is_v2 == 1:
            return ShareAccount_V2_AccessLevel[access_level]

        else:
            return ShareAccount_V1_AccessLevel[access_level]

    @classmethod
    async def _from_json(
        cls: ShareAccount, obj, auth: dmda.DomoAuth, is_v2: bool = False
    ):
        return cls(
            entity=await cls._get_entity(obj, auth=auth),
            auth=auth,
            access_level=cls._get_access_level(obj["accessLevel"], is_v2),
        )


@dataclass
class Account_Accesslist:
    account: DomoAccount
    auth: dmda.DomoAuth
    domo_users = None
    domo_groups = None

# %% ../../nbs/classes/50_DomoAccount.ipynb 50
@patch_to(DomoAccount)
async def get_accesslist(
    self: DomoAccount,
    auth: dmda.DomoAuth = None,
    debug_api: bool = False,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
):
    auth = auth or self.auth
    res = await account_routes.get_account_accesslist(
        auth=auth, account_id=self.id, debug_api=debug_api, session=session
    )

    if return_raw:
        return res

    is_v2 = await self.is_feature_accountsv2_enabled()

    self.accesslist = await ce.gather_with_concurrency(
        *[
            Account_Accesslist_Share._from_json(obj=obj, auth=auth, is_v2=is_v2)
            for obj in res.response["list"]
        ],
        n=10,
    )
    return self.accesslist

# %% ../../nbs/classes/50_DomoAccount.ipynb 54
@patch_to(DomoAccounts, cls_method=True)
async def upsert_account(
    cls: DomoAccounts,
    auth: dmda.DomoAuth,
    account_config: AccountConfig = None,
    account_name: str = None,
    account_id: str = None,
    debug_api: bool = False,
    debug_prn: bool = False,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
):
    """search for an account and upsert it"""

    if not account_name and not account_id:
        raise UpsertAccount_MatchCriteria(domo_instance=auth.domo_instance)

    acc = None
    res = None

    if account_id:
        acc = await DomoAccounts.get_accounts(account_id=account_id, auth=auth)

        if acc and account_name:
            if debug_prn:
                print(f"upsertting {acc.id}:  updating account_name")
            res = await acc.update_name(
                account_name=account_name, debug_api=debug_api, return_raw=return_raw
            )

    if account_name and acc is None:
        acc = await DomoAccounts.get_accounts(
            account_name=account_name,
            auth=auth,
            account_type_str=(account_config and account_config.data_provider_type)
            or None,
            # is_suppress_undefined_provider_type = True
        )

        if isinstance(acc, list) and len(acc) > 0 and isinstance(acc[0], DomoAccount):
            acc = acc[0]

        else:
            acc = None

    if acc and account_config:  # upsert account
        acc.config = account_config

        if debug_prn:
            print(f"upsertting {acc.id}:  updating config")

        res = await acc.update_config(debug_api=debug_api, return_raw=return_raw)

    if return_raw and acc:
        return res

    if not acc:
        if debug_prn:
            print(f"creating account {account_name} in {auth.domo_instance}")

        acc = await DomoAccount.create_account(
            account_name=account_name,
            config=account_config,
            auth=auth,
            debug_api=debug_api,
            return_raw=return_raw,
        )

    return acc

# %% ../../nbs/classes/50_DomoAccount.ipynb 57
@patch_to(DomoAccount)
async def upsert_share_account_user(
    self: DomoAccount,
    domo_user,
    auth: dmda.DomoAuth = None,
    is_v2: bool = None,
    access_level: ShareAccount = None,  # will default to Read
    debug_api: bool = False,
    debug_prn: bool = False,
    session: httpx.AsyncClient = None,
):
    auth = auth or self.auth

    ls_share = await account_routes.get_account_accesslist(
        auth=auth, account_id=self.id
    )
    res = None

    if domo_user:
        user_id = domo_user.id
        found_user = next(
            (
                obj
                for obj in ls_share.response["list"]
                if obj["id"] == user_id and obj["type"] == "USER"
            ),
            None,
        )
        if not found_user:
            res = await self.share(
                domo_user=domo_user,
                auth=auth,
                access_level=access_level,
                debug_api=debug_api,
                debug_prn=debug_prn,
                session=session,
            )

    return res


@patch_to(DomoAccount)
async def upsert_share_account_group(
    self: DomoAccount,
    domo_group,
    auth: dmda.DomoAuth = None,
    is_v2: bool = None,
    access_level: ShareAccount = None,  # will default to Read
    debug_api: bool = False,
    debug_prn: bool = False,
    session: httpx.AsyncClient = None,
):
    auth = auth or self.auth

    ls_share = await account_routes.get_account_accesslist(
        auth=auth, account_id=self.id
    )
    res = None

    if domo_group:
        group_id = domo_group.id
        found_group = next(
            (
                obj
                for obj in ls_share.response["list"]
                if obj["id"] == group_id and obj["type"] == "GROUP"
            ),
            None,
        )
        if not found_group:
            res = await self.share(
                domo_group=domo_group,
                auth=auth,
                access_level=access_level,
                debug_api=debug_api,
                debug_prn=debug_prn,
                session=session,
            )

    return res
