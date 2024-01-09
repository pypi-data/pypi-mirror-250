# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/classes/50_DomoPage.ipynb.

# %% auto 0
__all__ = ['DomoPage', 'DomoPages', 'Page_NoAccess']

# %% ../../nbs/classes/50_DomoPage.ipynb 2
from nbdev.showdoc import patch_to
from dataclasses import dataclass, field

import asyncio
import httpx

import domolibrary.client.Logger as lg
import domolibrary.client.DomoError as de
import domolibrary.client.DomoAuth as dmda
import domolibrary.classes.DomoPage_Content as dmpg_c
import domolibrary.routes.page as page_routes

import domolibrary.utils.DictDot as util_dd
import domolibrary.utils.chunk_execution as ce

# %% ../../nbs/classes/50_DomoPage.ipynb 3
from ..routes.page import PageRetrieval_byId_Error

# %% ../../nbs/classes/50_DomoPage.ipynb 6
@dataclass(
    # frozen = True
)
class DomoPage:
    id: int
    title: str = None
    top_page_id: int = None
    parent_page_id: int = None
    auth: dmda.DomoAuth = field(default=None, repr=False)
    is_locked: bool = None

    collections: list = field(default_factory=list)

    owners: list = field(default_factory=list)
    cards: list = field(default_factory=list)

    custom_attributes: dict = field(default_factory=dict)

    # parent_page: dict = None  # DomoPage
    # top_page: dict = None  # DomoPage
    # children: list = field(default_factory=list)
    # parent_hierarchy: [dict] = None
    # flat_children: list = None

    layout: dmpg_c.PageLayout = field(default_factory=dict)

    def display_url(self):
        return f"https://{self.auth.domo_instance}.domo.com/page/{self.id}"

    async def _get_domo_owners_from_dd(self, owners: util_dd.DictDot):
        if not owners or len(owners) == 0:
            return []

        import domolibrary.classes.DomoUser as dmu
        import domolibrary.classes.DomoGroup as dmg

        domo_groups = []
        domo_users = []

        owner_group_ls = [
            owner.id for owner in owners if owner.type == "GROUP" and owner.id
        ]

        if len(owner_group_ls) > 0:
            domo_groups = await ce.gather_with_concurrency(
                n=60,
                *[
                    dmg.DomoGroup.get_by_id(group_id=group_id, auth=self.auth)
                    for group_id in owner_group_ls
                ],
            )

        owner_user_ls = [
            owner.id for owner in owners if owner.type == "USER" and owner.id
        ]

        if len(owner_user_ls) > 0:
            domo_users = await dmu.DomoUsers.by_id(
                user_ids=owner_user_ls, only_allow_one=False, auth=self.auth
            )

        owner_ce = (domo_groups or []) + (domo_users or [])

        res = []
        for owner in owner_ce:
            if isinstance(owner, list):
                [res.append(member) for member in owner]
            else:
                res.append(owner)

        return res

# %% ../../nbs/classes/50_DomoPage.ipynb 7
@patch_to(DomoPage, cls_method=True)
async def _from_adminsummary(cls, page_obj, auth: dmda.DomoAuth):
    import domolibrary.classes.DomoCard as dmc

    dd = page_obj

    if isinstance(page_obj, dict):
        dd = util_dd.DictDot(page_obj)

    pg = cls(
        id=int(dd.id or dd.pageId),
        title=dd.title or dd.pageTitle,
        parent_page_id=int(dd.parentPageId) if dd.parentPageId else None,
        top_page_id=int(dd.topPageId) if dd.topPageId else None,
        collections=dd.collections,
        is_locked=dd.locked,
        auth=auth,
    )

    if dd.page and dd.page.owners and len(dd.page.owners) > 0:
        pg.owners = await pg._get_domo_owners_from_dd(dd.page.owners)

    if dd.cards and len(dd.cards) > 0:
        pg.cards = await ce.gather_with_concurrency(
            n=60,
            *[dmc.DomoCard.get_from_id(id=card.id, auth=auth) for card in dd.cards],
        )

    return pg

# %% ../../nbs/classes/50_DomoPage.ipynb 8
@patch_to(DomoPage, cls_method=True)
async def _from_bootstrap(cls: DomoPage, page_obj, auth: dmda.DomoAuth = None):
    dd = page_obj
    if isinstance(page_obj, dict):
        dd = util_dd.DictDot(page_obj)

    pg = cls(id=int(dd.id), title=dd.title, auth=auth)

    if isinstance(dd.owners, list) and len(dd.owners) > 0:
        pg.owners = await pg._get_domo_owners_from_dd(dd.owners)

    if isinstance(dd.children, list) and len(dd.children) > 0:
        pg.children = await ce.gather_with_concurrency(
            n=60,
            *[
                cls._from_bootstrap(page_obj=child_dd, auth=auth)
                for child_dd in dd.children
                if child_dd.type == "page"
            ],
        )

        [print(other_dd) for other_dd in dd.children if other_dd.type != "page"]

    return pg

# %% ../../nbs/classes/50_DomoPage.ipynb 10
@dataclass
class DomoPages:
    @classmethod
    async def get_pages(
        cls,
        auth=dmda.DomoAuth,
        return_raw: bool = False,
        debug_loop: bool = False,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
    ):
        """use admin_summary to retrieve all pages in an instance -- regardless of user access
        NOTE: some Page APIs will not return results if page access isn't explicitly shared
        """
        is_close_session = False if session else True

        session = session or httpx.AsyncClient()

        try:
            res = await page_routes.get_pages_adminsummary(
                auth=auth, debug_loop=False, debug_api=False, session=session
            )

            if return_raw:
                return res

            if not res.is_success:
                raise Exception("unable to retrieve pages")

            return await ce.gather_with_concurrency(
                n=60,
                *[
                    DomoPage._from_adminsummary(page_obj, auth=auth)
                    for page_obj in res.response
                ],
            )

        finally:
            if is_close_session:
                await session.aclose()

# %% ../../nbs/classes/50_DomoPage.ipynb 14
@patch_to(DomoPage, cls_method=True)
async def _from_content_stacks_v3(cls: DomoPage, page_obj, auth: dmda.DomoAuth = None):
    # import domolibrary.classes.DomoCard as dc

    dd = page_obj
    if isinstance(page_obj, dict):
        dd = util_dd.DictDot(page_obj)

    pg = cls(
        id=int(dd.id),
        title=dd.title,
        parent_page_id=int(dd.page.parentPageId) if dd.page.parentPageId else None,
        collections=dd.collections,
        auth=auth,
    )

    if hasattr(dd, "pageLayoutV4") and dd.pageLayoutV4 is not None:
        pg.layout = dmpg_c.PageLayout._from_json(dd=dd.pageLayoutV4)

    if dd.page.owners and len(dd.page.owners) > 0:
        pg.owners = await pg._get_domo_owners_from_dd(dd.page.owners)

    # if dd.cards and len(dd.cards) > 0:
    #     pg.cards = await asyncio.gather(
    #         *[dc.DomoCard.get_from_id(id=card.id, auth=auth) for card in dd.cards])

    return pg


class DomoPage_GetRecursive(de.DomoError):
    def __init__(
        self,
        include_recursive_children,
        include_recursive_parents,
        page_id,
        domo_instance,
        function_name,
        parent_class,
    ):
        super().__init__(
            domo_instance=domo_instance,
            function_name=function_name,
            parent_class=parent_class,
            message=f"error retrieving {page_id} can only trace parents OR children recursively but not both. include_recursive_children : {include_recursive_children}, include_recursive_parents: {include_recursive_parents}",
        )


@patch_to(DomoPage, cls_method=True)
async def get_by_id(
    cls: DomoPage,
    page_id: str,
    auth: dmda.DomoAuth,
    return_raw: bool = False,
    debug_api: bool = False,
    include_layout: bool = False,
    # if True, will drill down to all the Children.  Set to False to prevent calculating children
    include_recursive_children: bool = True,
    include_recursive_parents: bool = False,
):
    # can only trace upstream or downstream but not both
    if include_recursive_children and include_recursive_parents:
        traceback_details = lg.get_traceback()

        raise DomoPage_GetRecursive(
            include_recursive_children=include_recursive_children,
            include_recursive_parents=include_recursive_parents,
            page_id=page_id,
            domo_instance=auth.domo_instance,
            function_name=traceback_details.function_name,
            parent_class=cls.__name__,
        )

    res = await page_routes.get_page_by_id(
        auth=auth, page_id=page_id, debug_api=debug_api, include_layout=include_layout
    )

    if return_raw:
        return res

    if not res.is_success:
        return None

    pg = await cls._from_content_stacks_v3(page_obj=res.response, auth=auth)

    pg.custom_attributes["parent_page"] = None
    pg.custom_attributes["top_page"] = None

    if pg.parent_page_id and include_recursive_parents:
        pg.custom_attributes["parent_page"] = await cls.get_by_id(
            auth=auth,
            page_id=pg.parent_page_id,
            include_recursive_parents=include_recursive_parents,
            include_recursive_children=False,
        )

        if pg.custom_attributes["parent_page"]:
            pg.custom_attributes["parent_hierarchy"] = pg.get_parent_hierarchy()

            pg.custom_attributes["top_page"] = pg.custom_attributes["parent_hierarchy"][
                -1
            ]["page"]
            pg.top_page_id = pg.custom_attributes["parent_hierarchy"][-1]["page"].id

    if include_recursive_children:
        await pg.get_children(
            include_recursive_children=include_recursive_children,
        )
        pg.flat_children = pg.flatten_children()

    return pg


@patch_to(DomoPage)
def get_parent_hierarchy(self: DomoPage, path=None, hierarchy=0, results=None):
    results = results or []

    path = path or self.title

    results.append({"hierarchy": hierarchy, "path": path, "page": self})

    if self.custom_attributes["parent_page"]:
        path = f"{path} > {self.custom_attributes['parent_page'].title}"
        self.custom_attributes["parent_page"].get_parent_hierarchy(
            path, hierarchy + 1, results
        )

    return results


@patch_to(DomoPage)
async def get_children(self: DomoPage, include_recursive_children: bool = False):
    all_pages = await DomoPages.get_pages(auth=self.auth)

    self.children = await ce.gather_with_concurrency(
        n=10,
        *[
            DomoPage.get_by_id(
                page_id=page.id,
                auth=self.auth,
                include_recursive_children=include_recursive_children,
                include_recursive_parents=False,
            )
            for page in all_pages
            if page.parent_page_id == self.id
        ],
    )

    return self.children


@patch_to(DomoPage)
def flatten_children(self: DomoPage, path=None, hierarchy=0, results=None):
    results = results or []

    path = f"{path} > {self.title}" if path else self.title

    results.append({"hierarchy": hierarchy, "path": path, "page": self})

    if self.children:
        [
            child.flatten_children(path, hierarchy + 1, results)
            for child in self.children
        ]

    return results

# %% ../../nbs/classes/50_DomoPage.ipynb 22
class Page_NoAccess(de.DomoError):
    def __init__(self, page_id, page_title, domo_instance, function_name, parent_class):
        super().__init__(
            function_name=function_name,
            parent_class=parent_class,
            domo_instance=domo_instance,
            message=f'authenticated user doesn\'t have access to {page_id} - "{page_title}" contact owners to share access',
        )

# %% ../../nbs/classes/50_DomoPage.ipynb 23
@patch_to(DomoPage)
async def test_page_access(
    self: DomoPage,
    suppress_no_access_error: bool = False,  # suppresses error if user doesn't have access
    debug_api: bool = False,
    return_raw: bool = False,
):
    """throws an error if user doesn't have access to the page
    API returns the owners of the page
    """

    res = await page_routes.get_page_access_test(auth=self.auth, page_id=self.id)

    try:
        page_access = res.response.get("pageAccess")

        if not page_access:
            raise Page_NoAccess(
                page_id=self.id,
                page_title=self.title,
                domo_instance=self.auth.domo_instance,
                function_name=res.traceback_details.function_name,
                parent_class=self.__class__.__name__,
            )

    except Page_NoAccess as e:
        print(e)

        if not suppress_no_access_error:
            raise e

    return res

# %% ../../nbs/classes/50_DomoPage.ipynb 27
@patch_to(DomoPage)
async def get_accesslist(
    self,
    auth: dmda.DomoAuth = None,
    return_raw: bool = False,
    debug_api: bool = False,
):
    auth = auth or self.auth

    res = await page_routes.get_page_access_list(
        auth=auth,
        is_expand_users=True,
        page_id=self.id,
        debug_api=debug_api,
        debug_num_stacks_to_drop=2,
        parent_class=self.__class__.__name__,
    )

    if return_raw:
        return res

    if not res.is_success:
        raise Exception("error getting access list")

    import domolibrary.classes.DomoUser as dmu
    import domolibrary.classes.DomoGroup as dmg

    s = {
        "explicit_shared_user_count": res.response.get("explicitSharedUserCount"),
        "total_user_count": res.response.get("totalUserCount"),
    }

    user_ls = res.response.get("users", None)
    domo_users = []
    if user_ls and isinstance(user_ls, list) and len(user_ls) > 0:
        domo_users = await dmu.DomoUsers.by_id(
            user_ids=[user.get("id") for user in user_ls],
            only_allow_one=False,
            auth=auth,
        )

    group_ls = res.response.get("groups", None)
    domo_groups = []
    if group_ls and isinstance(group_ls, list) and len(group_ls) > 0:
        domo_groups = await ce.gather_with_concurrency(
            n=60,
            *[
                dmg.DomoGroup.get_by_id(group_id=group.get("id"), auth=auth)
                for group in group_ls
            ],
        )

    res = await self.test_page_access(suppress_no_access_error=True)
    owner_ls = res.response["owners"]  # from test_page_access

    for domo_user in domo_users:
        # isExplicitShare is set by the get_access_list API response
        domo_user.custom_attributes["is_explicit_share"] = next(
            (
                user_obj["isExplicitShare"]
                for user_obj in user_ls
                if int(user_obj.get("id")) == int(domo_user.id)
            )
        )

        # group membership is determined by get_access_list API response
        domo_user.custom_attributes["group_membership"] = [
            domo_group
            for group_obj in group_ls
            for domo_group in domo_groups
            if int(domo_user.id)
            in [int(user_obj["id"]) for user_obj in group_obj.get("users")]
            and domo_group.id == group_obj["id"]
        ]

        # isOwner determined by test_access API response and group membership
        domo_user.custom_attributes["is_owner"] = False

        # test ownership as a user
        match_owner = next(
            (
                owner_obj
                for owner_obj in owner_ls
                if int(owner_obj["id"]) == int(domo_user.id)
                and owner_obj["type"] == "USER"
            ),
            None,
        )

        match_group = next(
            (
                owner_obj
                for owner_obj in owner_ls
                if int(owner_obj["id"])
                in [
                    int(domo_group.id)
                    for domo_group in domo_user.custom_attributes["group_membership"]
                ]
                and owner_obj["type"] == "GROUP"
            ),
            None,
        )

        if match_owner or match_group:
            domo_user.custom_attributes["is_owner"] = True

    # group ownership is confirmed test_access API
    for domo_group in domo_groups:
        match_owner = next(
            (
                owner_obj
                for owner_obj in owner_ls
                if int(owner_obj["id"]) == int(domo_group.id)
                and owner_obj["type"] == "GROUP"
            ),
            None,
        )

        domo_group.custom_attributes["is_owner"] = True if match_owner else False

    return {
        **s,
        "domo_users": domo_users,
        "domo_groups": domo_groups,
    }

# %% ../../nbs/classes/50_DomoPage.ipynb 30
@patch_to(DomoPage)
async def share(
    self: DomoPage,
    auth: dmda.DomoAuth = None,
    domo_users: list = None,  # DomoUsers to share page with,
    domo_groups: list = None,  # DomoGroups to share page with
    message: str = None,  # message for automated email
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    import domolibrary.routes.datacenter as datacenter_routes

    if domo_groups:
        domo_groups = domo_groups if isinstance(domo_groups, list) else [domo_groups]
    if domo_users:
        domo_users = domo_users if isinstance(domo_users, list) else [domo_users]

    res = await datacenter_routes.share_resource(
        auth=auth or self.auth,
        resource_ids=[self.id],
        resource_type=datacenter_routes.ShareResource_Enum.PAGE,
        group_ids=[group.id for group in domo_groups] if domo_groups else None,
        user_ids=[user.id for user in domo_users] if domo_users else None,
        message=message,
        debug_api=debug_api,
        session=session,
    )

    return res

# %% ../../nbs/classes/50_DomoPage.ipynb 33
@patch_to(DomoPage, cls_method=True)
async def get_cards(
    cls,
    auth: dmda.DomoAuth,
    page_id,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    import domolibrary.classes.DomoCard as dc

    res = await page_routes.get_page_definition(
        auth=auth, page_id=page_id, debug_api=debug_api, session=session
    )

    if res.status != 200:
        raise Exception(
            f"unable to retrieve page definition for {page_id} in {auth.domo_instance}"
        )

    if len(res.response.get("cards")) == 0:
        return []

    return await ce.gather_with_concurrency(
        n=60,
        *[
            dc.DomoCard.get_by_id(card_id=card["id"], auth=auth)
            for card in res.response.get("cards")
        ],
    )


@patch_to(DomoPage, cls_method=True)
async def get_datasets(
    cls,
    auth: dmda.DomoAuth,
    page_id,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    import domolibrary.classes.DomoDataset as dmds

    res = await page_routes.get_page_definition(
        auth=auth, page_id=page_id, debug_api=debug_api, session=session
    )

    if res.status != 200:
        raise Exception(
            f"unable to retrieve datasets for page {page_id} in {auth.domo_instance}"
        )

    if len(res.response.get("cards")) == 0:
        return []

    return await ce.gather_with_concurrency(
        n=60,
        *[
            dmds.DomoDataset.get_from_id(dataset_id=ds.get("dataSourceId"), auth=auth)
            for card in res.response.get("cards")
            for ds in card.get("datasources")
        ],
    )

# %% ../../nbs/classes/50_DomoPage.ipynb 36
from datetime import datetime
from domolibrary.utils import convert


@patch_to(DomoPage, cls_method=True)
async def update_layout(
    cls, auth: dmda.DomoAuth, body: dict, layout_id: str, debug_api: bool = False
):
    datetime_now = datetime.now()
    start_time_epoch = convert.convert_datetime_to_epoch_millisecond(datetime_now)

    res_writelock = await page_routes.put_writelock(
        auth=auth,
        layout_id=layout_id,
        user_id=auth.user_id,
        epoch_time=start_time_epoch,
    )
    if res_writelock.status == 200:
        res = await page_routes.update_page_layout(
            auth=auth, body=body, layout_id=layout_id, debug_api=debug_api
        )

        if not res.is_success:
            return False

        res_writelock = await page_routes.delete_writelock(
            auth=auth, layout_id=layout_id
        )
        if res_writelock.status != 200:
            return False

    else:
        return False

    return True

# %% ../../nbs/classes/50_DomoPage.ipynb 39
@patch_to(DomoPage, cls_method=True)
async def add_page_owner(
    cls,
    auth: dmda.DomoAuth,
    page_id_ls: [],  # Page IDs to be updated by owner,
    group_id_ls: [],  # DomoGroup IDs to share page with
    user_id_ls: [],  # DomoUser IDs to share page with
    note: str = None,  # message for automated email
    send_email: bool = False,  # send or not email to the new owners
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    res = await page_routes.add_page_owner(
        auth=auth,
        page_id_ls=page_id_ls,
        group_id_ls=group_id_ls,
        user_id_ls=user_id_ls,
        note=note,
        send_email=send_email,
        debug_api=debug_api,
        session=session,
    )

    return res
