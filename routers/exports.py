from schemas import TransactionSchema as tschema
from config import database, env_handler
from pathlib import Path
from datetime import datetime
from sqlalchemy import text
from fastapi import APIRouter
from fastapi import Response, status, HTTPException, Header
from typing import Union
import pandas as pd
import requests
import sys

sys.path.append("..")


# Create a router
router = APIRouter(prefix="/export", tags=["Exports"])

# Read the SQL file and create a text object
path = Path("sql/TransactionReport.sql")
query = text(open(path).read())


def authenticate_request(request):
    # Get the Sanctum token from the request headers
    token = request.headers.get("Authorization")
    # return token

    # If the token is not present, return an error
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    # Verify the token using the Sanctum API
    try:
        response = requests.post(
            f"{env_handler.env('API', 'API_ENDPOINT')}/admin/sanctum/token/verify",
            headers={"Authorization": token},
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )


@router.post("/transactions/{status}/{payin_type}")
async def transactions_export(
    request: tschema.Transaction,
    status: tschema.StatusTypeEnum,
    payin_type: tschema.PayinTypeEnum,
    Authorization: Union[str, None] = Header(default=None),
):
    """Queries the transactions table, returns csv file as query result."""
    # Authenticate user
    authenticate_request(Authorization)

    from_param = datetime.strptime(request.from_, "%Y-%m-%d")
    to_param = datetime.strptime(request.to, "%Y-%m-%d")

    parameters = {
        "from_param": str(from_param),
        "to_param": str(to_param),
        "payin_param": str(payin_type),
        "status_param": str(status),
    }

    # Start the server connection
    engine = database.start_server()

    # Execute the query and retrieve the results as a DataFrame
    df = pd.read_sql(query, engine, params=parameters)

    # Stop the server connection
    database.stop_server()

    # Convert the DataFrame to a CSV string
    csv = df.to_csv(index=False)

    # Return the CSV string as the response body
    return Response(
        csv,
        media_type="text/csv",
        headers={
            f"Content-disposition": f"attachment; filename=transactions_{from_param}_to_{to_param}.csv"
        },
    )
