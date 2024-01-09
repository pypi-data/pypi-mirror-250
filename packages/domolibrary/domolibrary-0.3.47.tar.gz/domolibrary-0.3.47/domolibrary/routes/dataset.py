# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/routes/dataset.ipynb.

# %% auto 0
__all__ = ['DatasetNotFoundError', 'QueryRequestError', 'query_dataset_public', 'query_dataset_private', 'get_dataset_by_id',
           'get_schema', 'alter_schema', 'set_dataset_tags', 'UploadDataError', 'upload_dataset_stage_1',
           'upload_dataset_stage_2_file', 'upload_dataset_stage_2_df', 'upload_dataset_stage_3', 'index_dataset',
           'index_status', 'generate_list_partitions_body', 'list_partitions', 'generate_create_dataset_body', 'create',
           'delete_partition_stage_1', 'delete_partition_stage_2', 'delete', 'ShareDataset_AccessLevelEnum',
           'generate_share_dataset_payload', 'ShareDataset_Error', 'share_dataset']

# %% ../../nbs/routes/dataset.ipynb 3
from typing import Optional
from enum import Enum

import io
import pandas as pd

import httpx

import domolibrary.client.get_data as gd
import domolibrary.client.ResponseGetData as rgd
import domolibrary.client.DomoAuth as dmda
import domolibrary.client.DomoError as de

# %% ../../nbs/routes/dataset.ipynb 5
class DatasetNotFoundError(de.DomoError):
    def __init__(
        self,
        dataset_id,
        domo_instance,
        status=None,
        parent_class=None,
        function_name=None,
    ):
        message = f"dataset - {dataset_id} not found"

        super().__init__(
            message,
            status=status,
            domo_instance=domo_instance,
            function_name=function_name,
            parent_class=parent_class,
        )

# %% ../../nbs/routes/dataset.ipynb 6
class QueryRequestError(de.DomoError):
    def __init__(
        self,
        dataset_id,
        domo_instance,
        sql,
        status=None,
        message="",
        parent_class=None,
        function_name=None,
    ):
        message = f"dataset - {dataset_id} received a bad request {message}.  Check your SQL \n {sql}"

        super().__init__(
            message,
            status=status,
            domo_instance=domo_instance,
            parent_class=parent_class,
            function_name=function_name,
        )


# typically do not use
async def query_dataset_public(
    dev_auth: dmda.DomoDeveloperAuth,
    dataset_id: str,
    sql: str,
    session: httpx.AsyncClient,
    debug_api: bool = False,
):
    """query for hitting public apis, requires client_id and secret authentication"""

    url = f"https://api.domo.com/v1/datasets/query/execute/{dataset_id}?IncludeHeaders=true"

    body = {"sql": sql}

    return await gd.get_data(
        auth=dev_auth,
        url=url,
        method="POST",
        body=body,
        session=session,
        debug_api=debug_api,
    )


async def query_dataset_private(
    auth: dmda.DomoAuth,  # DomoFullAuth or DomoTokenAuth
    dataset_id: str,
    sql: str,
    session: Optional[httpx.AsyncClient] = None,
    loop_until_end: bool = False,  # retrieve all available rows
    limit=100,  # maximum rows to return per request.  refers to PAGINATION
    skip=0,
    maximum=100,  # equivalent to the LIMIT or TOP clause in SQL, the number of rows to return total
    filter_pdp_policy_id_ls: [int] = None,
    debug_api: bool = False,
    debug_loop: bool = False,
    timeout: int = 10,
    parent_class=None,
    debug_num_stacks_to_drop=1,
):
    """execute SQL queries against private APIs, requires DomoFullAuth or DomoTokenAuth"""

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/execute/{dataset_id}"

    offset_params = {
        "offset": "offset",
        "limit": "limit",
    }

    # def body_fn(skip, limit):
    #     return {"sql": f"{sql} limit {limit} offset {skip}"}

    def body_fn(skip, limit, body=None):
        body = {"sql": f"{sql} limit {limit} offset {skip}"}

        if filter_pdp_policy_id_ls:
            body.update(
                {
                    "context": {
                        "dataControlContext": {
                            "filterGroupIds": filter_pdp_policy_id_ls,
                            "previewPdp": True,
                        }
                    }
                }
            )

        return body

    def arr_fn(res) -> pd.DataFrame:
        rows_ls = res.response.get("rows")
        columns_ls = res.response.get("columns")
        output = []
        for row in rows_ls:
            new_row = {}
            for index, column in enumerate(columns_ls):
                new_row[column] = row[index]
            output.append(new_row)
            # pd.DataFrame(data=res.response.get('rows'), columns=res.response.get('columns'))
        return output

    res = await gd.looper(
        auth=auth,
        method="POST",
        url=url,
        arr_fn=arr_fn,
        offset_params=offset_params,
        limit=limit,
        skip=skip,
        maximum=maximum,
        session=session,
        body_fn=body_fn,
        debug_api=debug_api,
        debug_loop=debug_loop,
        loop_until_end=loop_until_end,
        timeout=timeout,
        parent_class=parent_class,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if res.status == 404 and res.response == "Not Found":
        raise DatasetNotFoundError(
            dataset_id=dataset_id,
            domo_instance=auth.domo_instance,
            status=res.status,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
        )

    if res.status == 400 and res.response == "Bad Request":
        raise QueryRequestError(
            dataset_id=dataset_id,
            domo_instance=auth.domo_instance,
            sql=sql,
            status=res.status,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
        )

    if not res.is_success:
        raise QueryRequestError(
            dataset_id=dataset_id,
            domo_instance=auth.domo_instance,
            sql=sql,
            message=res.response,
            status=res.status,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
        )

    return res

# %% ../../nbs/routes/dataset.ipynb 9
async def get_dataset_by_id(
    dataset_id: str,  # dataset id from URL
    auth: Optional[dmda.DomoAuth] = None,  # requires full authentication
    debug_api: bool = False,  # for troubleshooting API request
    session: Optional[httpx.AsyncClient] = None,
    parent_class: str = None,
    debug_num_stacks_to_drop=1,
) -> rgd.ResponseGetData:  # returns metadata about a dataset
    """retrieve dataset metadata"""

    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        session=session,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if res.status == 404 and res.response == "Not Found":
        raise DatasetNotFoundError(
            dataset_id=dataset_id,
            domo_instance=auth.domo_instance,
            status=res.status,
            parent_class=parent_class,
            function_name=res.traceback_details.function_name,
        )

    return res

# %% ../../nbs/routes/dataset.ipynb 12
async def get_schema(
    auth: dmda.DomoAuth,
    dataset_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    parent_class=None,
) -> rgd.ResponseGetData:
    """retrieve the schema for a dataset"""

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/datasources/{dataset_id}/schema/indexed?includeHidden=false"

    return await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

# %% ../../nbs/routes/dataset.ipynb 15
async def alter_schema(
    auth: dmda.DomoAuth,
    schema_obj: dict,
    dataset_id: str,
    debug_api: bool = False,
    parent_class: str = None,
    debug_num_stacks_to_drop: int = 1,
) -> rgd.ResponseGetData:
    """retrieve the schema for a dataset"""

    url = f"https://{auth.domo_instance}.domo.com/api/data/v2/datasources/{dataset_id}/schemas"

    return await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        body=schema_obj,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

# %% ../../nbs/routes/dataset.ipynb 17
async def set_dataset_tags(
    auth: dmda.DomoFullAuth,
    tag_ls: [str],  # complete list of tags for dataset
    dataset_id: str,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    return_raw: bool = False,
    parent_class: str = None,
    debug_num_stacks_to_drop: int = 1,
):
    """REPLACE tags on this dataset with a new list"""

    url = f"https://{auth.domo_instance}.domo.com/api/data/ui/v3/datasources/{dataset_id}/tags"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        debug_api=debug_api,
        body=tag_ls,
        session=session,
        return_raw=return_raw,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    if res.status == 200:
        res.set_response(
            response=f'Dataset {dataset_id} tags updated to [{ ", ".join(tag_ls) }]'
        )

    return res

# %% ../../nbs/routes/dataset.ipynb 20
class UploadDataError(de.DomoError):
    """raise if unable to upload data to Domo"""

    def __init__(
        self, stage_num: int, dataset_id: str, status, message, domo_instance: str
    ):
        message = f"error uploading data during Stage { stage_num} - {message}"

        super().__init__(
            entity_id=dataset_id,
            message=message,
            status=status,
            domo_instance=domo_instance,
        )

# %% ../../nbs/routes/dataset.ipynb 21
async def upload_dataset_stage_1(
    auth: dmda.DomoAuth,
    dataset_id: str,
    #  restate_data_tag: str = None, # deprecated
    partition_tag: str = None,  # synonymous with data_tag
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """preps dataset for upload by creating an upload_id (upload session key) pass to stage 2 as a parameter"""

    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}/uploads"

    # base body assumes no paritioning
    body = {"action": None, "appendId": None}

    params = None

    if partition_tag:
        # params = {'dataTag': restate_data_tag or data_tag} # deprecated
        params = {"dataTag": partition_tag}
        body.update({"appendId": "latest"})

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="POST",
        body=body,
        session=session,
        debug_api=debug_api,
        params=params,
    )

    if not res.is_success:
        raise UploadDataError(
            stage_num=1,
            dataset_id=dataset_id,
            domo_instance=auth.domo_instance,
            status=res.status,
            message=res.response,
        )

    if return_raw:
        return res

    upload_id = res.response.get("uploadId")

    if not upload_id:
        raise UploadDataError(
            stage_num=1,
            dataset_id=dataset_id,
            domo_instance=auth.domo_instance,
            status=res.status,
            message="no upload_id",
        )

    res.response = upload_id

    return res

# %% ../../nbs/routes/dataset.ipynb 23
async def upload_dataset_stage_2_file(
    auth: dmda.DomoAuth,
    dataset_id: str,
    upload_id: str,  # must originate from  a stage_1 upload response
    data_file: Optional[io.TextIOWrapper] = None,
    session: Optional[httpx.AsyncClient] = None,
    # only necessary if streaming multiple files into the same partition (multi-part upload)
    part_id: str = 2,
    debug_api: bool = False,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}/uploads/{upload_id}/parts/{part_id}"

    body = data_file

    res = await gd.get_data(
        url=url,
        method="PUT",
        auth=auth,
        content_type="text/csv",
        body=body,
        session=session,
        debug_api=debug_api,
    )

    if not res.is_success:
        raise UploadDataError(
            stage_num=2,
            dataset_id=dataset_id,
            domo_instance=auth.domo_instance,
            status=res.status,
            message=res.response,
        )

    res.upload_id = upload_id
    res.dataset_id = dataset_id
    res.part_id = part_id

    return res

# %% ../../nbs/routes/dataset.ipynb 24
async def upload_dataset_stage_2_df(
    auth: dmda.DomoAuth,
    dataset_id: str,
    upload_id: str,  # must originate from  a stage_1 upload response
    upload_df: pd.DataFrame,
    session: Optional[httpx.AsyncClient] = None,
    part_id: str = 2,  # only necessary if streaming multiple files into the same partition (multi-part upload)
    debug_api: bool = False,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}/uploads/{upload_id}/parts/{part_id}"

    body = upload_df.to_csv(header=False, index=False)

    # if debug:
    #     print(body)

    res = await gd.get_data(
        url=url,
        method="PUT",
        auth=auth,
        content_type="text/csv",
        body=body,
        session=session,
        debug_api=debug_api,
    )

    if not res.is_success:
        raise UploadDataError(
            stage_num=2,
            dataset_id=dataset_id,
            domo_instance=auth.domo_instance,
            status=res.status,
            message=res.response,
        )

    res.upload_id = upload_id
    res.dataset_id = dataset_id
    res.part_id = part_id

    return res

# %% ../../nbs/routes/dataset.ipynb 25
async def upload_dataset_stage_3(
    auth: dmda.DomoAuth,
    dataset_id: str,
    upload_id: str,  # must originate from  a stage_1 upload response
    session: Optional[httpx.AsyncClient] = None,
    update_method: str = "REPLACE",  # accepts REPLACE or APPEND
    #  restate_data_tag: str = None, # deprecated
    partition_tag: str = None,  # synonymous with data_tag
    is_index: bool = False,  # index after uploading
    debug_api: bool = False,
) -> rgd.ResponseGetData:
    """commit will close the upload session, upload_id.  this request defines how the data will be loaded into Adrenaline, update_method
    has optional flag for indexing dataset.
    """

    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}/uploads/{upload_id}/commit"

    body = {"index": is_index, "action": update_method}

    if partition_tag:
        body.update(
            {
                "action": "APPEND",
                #  'dataTag': restate_data_tag or data_tag,
                #  'appendId': 'latest' if (restate_data_tag or data_tag) else None,
                "dataTag": partition_tag,
                "appendId": "latest" if partition_tag else None,
                "index": is_index,
            }
        )

    res = await gd.get_data(
        auth=auth,
        method="PUT",
        url=url,
        body=body,
        session=session,
        debug_api=debug_api,
    )

    if not res.is_success:
        raise UploadDataError(
            stage_num=3,
            dataset_id=dataset_id,
            domo_instance=auth.domo_instance,
            status=res.status,
            message=res.response,
        )

    res.upload_id = upload_id
    res.dataset_id = dataset_id

    return res

# %% ../../nbs/routes/dataset.ipynb 27
async def index_dataset(
    auth: dmda.DomoAuth,
    dataset_id: str,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
) -> rgd.ResponseGetData:
    """manually index a dataset"""

    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}/indexes"

    body = {"dataIds": []}

    return await gd.get_data(
        auth=auth,
        method="POST",
        body=body,
        url=url,
        session=session,
        debug_api=debug_api,
    )

# %% ../../nbs/routes/dataset.ipynb 28
async def index_status(
    auth: dmda.DomoAuth,
    dataset_id: str,
    index_id: str,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
) -> rgd.ResponseGetData:
    """get the completion status of an index"""

    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}/indexes/{index_id}/statuses"

    return await gd.get_data(
        auth=auth, method="GET", url=url, session=session, debug_api=debug_api
    )

# %% ../../nbs/routes/dataset.ipynb 30
def generate_list_partitions_body(limit=100, offset=0):
    return {
        "paginationFields": [
            {
                "fieldName": "datecompleted",
                "sortOrder": "DESC",
                "filterValues": {"MIN": None, "MAX": None},
            }
        ],
        "limit": limit,
        "offset": offset,
    }


async def list_partitions(
    auth: dmda.DomoAuth,
    dataset_id: str,
    body: dict = None,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_loop: bool = False,
):
    body = body or generate_list_partitions_body()

    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/datasources/{dataset_id}/partition/list"

    offset_params = {
        "offset": "offset",
        "limit": "limit",
    }

    def arr_fn(res) -> list[dict]:
        return res.response

    res = await gd.looper(
        auth=auth,
        method="POST",
        url=url,
        arr_fn=arr_fn,
        body=body,
        offset_params_in_body=True,
        offset_params=offset_params,
        loop_until_end=True,
        session=session,
        debug_loop=debug_loop,
        debug_api=debug_api,
    )

    if res.status == 404 and res.response == "Not Found":
        raise DatasetNotFoundError(
            dataset_id=dataset_id, domo_instance=auth.domo_instance, status=res.status
        )
    return res

# %% ../../nbs/routes/dataset.ipynb 32
def generate_create_dataset_body(
    dataset_name: str, dataset_type: str = "API", schema: dict = None
):
    schema = schema or {
        "columns": [
            {"type": "STRING", "name": "Friend"},
            {"type": "STRING", "name": "Attending"},
        ]
    }

    return {
        "userDefinedType": dataset_type,
        "dataSourceName": dataset_name,
        "schema": schema,
    }


async def create(
    auth: dmda.DomoAuth,
    dataset_name: str,
    dataset_type: str = "api",
    session: httpx.AsyncClient = None,
    schema: dict = None,
    debug_api: bool = False,
):
    body = generate_create_dataset_body(
        dataset_name=dataset_name, dataset_type=dataset_type, schema=schema
    )

    url = f"https://{auth.domo_instance}.domo.com/api/data/v2/datasources"

    return await gd.get_data(
        auth=auth,
        method="POST",
        url=url,
        body=body,
        session=session,
        debug_api=debug_api,
    )

# %% ../../nbs/routes/dataset.ipynb 35
async def delete_partition_stage_1(
    auth: dmda.DomoAuth,
    dataset_id: str,
    dataset_partition_id: str,
    debug_api: bool = False,
):
    # Delete partition has 3 stages
    # Stage 1. This marks the data version associated with the partition tag as deleted.  It does not delete the partition tag or remove the association between the partition tag and data version.  There should be no need to upload an empty file – step #3 will remove the data from Adrenaline.
    # update on 9/9/2022 based on the conversation with Greg Swensen
    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/datasources/{dataset_id}/tag/{dataset_partition_id}/data"

    return await gd.get_data(auth=auth, method="DELETE", url=url, debug_api=debug_api)


# Stage 2. This will remove the partition association so that it doesn’t show up in the list call.  Technically, this is not required as a partition against a deleted data version will not count against the 400 partition limit, but as the current partitions api doesn’t make that clear, cleaning these up will make it much easier for you to manage.

# %% ../../nbs/routes/dataset.ipynb 36
async def delete_partition_stage_2(
    auth: dmda.DomoAuth,
    dataset_id: str,
    dataset_partition_id: str,
    debug_api: bool = False,
):
    url = f"https://{auth.domo_instance}.domo.com/api/query/v1/datasources/{dataset_id}/partition/{dataset_partition_id}"

    return await gd.get_data(auth=auth, method="DELETE", url=url, debug_api=debug_api)

# %% ../../nbs/routes/dataset.ipynb 37
async def delete(
    auth: dmda.DomoAuth,
    dataset_id: str,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
):
    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}?deleteMethod=hard"

    return await gd.get_data(
        auth=auth, method="DELETE", url=url, session=session, debug_api=debug_api
    )

# %% ../../nbs/routes/dataset.ipynb 38
class ShareDataset_AccessLevelEnum(Enum):
    CO_OWNER = "CO_OWNER"
    CAN_EDIT = "CAN_EDIT"
    CAN_SHARE = "CAN_SHARE"


def generate_share_dataset_payload(
    entity_type,  # USER or GROUP
    entity_id,
    access_level: ShareDataset_AccessLevelEnum = ShareDataset_AccessLevelEnum.CAN_SHARE,
    is_send_email: bool = False,
):
    return {
        "permissions": [
            {"type": entity_type, "id": entity_id, "accessLevel": access_level.value}
        ],
        "sendEmail": is_send_email,
    }

# %% ../../nbs/routes/dataset.ipynb 39
class ShareDataset_Error(de.DomoError):
    def __init__(
        self,
        dataset_id,
        status,
        response,
        domo_instance,
        parent_class=None,
        function_name=None,
    ):
        message = f"error sharing dataset {dataset_id} - {response}"

        super().__init__(
            status=status,
            domo_instance=domo_instance,
            message=message,
            parent_class=parent_class,
            function_name=function_name,
        )


async def share_dataset(
    auth: dmda.DomoAuth,
    dataset_id: str,
    body: dict,
    session: httpx.AsyncClient = None,
    debug_api=False,
    parent_class=None,
    debug_num_stacks_to_drop=1,
):
    url = f"https://{auth.domo_instance}.domo.com/api/data/v3/datasources/{dataset_id}/share"

    res = await gd.get_data(
        auth=auth,
        method="POST",
        url=url,
        body=body,
        session=session,
        debug_api=debug_api,
        parent_class=parent_class,
        num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if not res.is_success:
        raise ShareDataset_Error(
            dataset_id=dataset_id,
            status=res.status,
            response=res.response,
            domo_instance=auth.domo_instance,
        )

    update_user_ls = [f"{user['type']} - {user['id']}" for user in body["permissions"]]

    res.response = (
        f"updated access list { ', '.join(update_user_ls)} added to {dataset_id}"
    )
    return res
