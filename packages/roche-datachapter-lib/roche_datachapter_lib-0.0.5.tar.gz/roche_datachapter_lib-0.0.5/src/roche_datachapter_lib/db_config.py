"""DB config"""
from typing import List, Dict, Any
import dataclasses
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError

ENV_VAR_NAMES = ["SQLSERVER_SERVER", "SQLSERVER_USER", "SQLSERVER_PWD",
                 "SQLSERVER_LATAM_AR_DB", "SQLSERVER_LATAM_AR_DEV_DB",
                 "SQLSERVER_LATAM_AR_FARMADB_DB", "SQLSERVER_LATAM_AR_SAND_DB",
                 "SQLSERVER_LATAM_AR_STAGING_DB", "SQLSERVER_LATAM_UY_DB",
                 "SQLSERVER_LATAM_UY_STAGING_DB", "GODW_SERVER", "GODW_PORT",
                 "GODW_USER", "GODW_PASSWORD", "GODW_SERVICENAME", "GODW_ORACLE_INSTANT_CLIENT_PATH",
                 "SAPDWP06_SERVER", "SAPDWP06_PORT", "SAPDWP06_USER", "SAPDWP06_PASSWORD", "SAPDWP06_DB",
                 "REXIS_SALES_SERVER", "REXIS_SALES_DB", "REXIS_SERVICES_SERVER", "REXIS_SERVICES_DB"]

for env_var_name in ENV_VAR_NAMES:
    value = environ.get(env_var_name)

    if value is not None:
        globals()[env_var_name] = value
    else:
        raise EnvironmentError(
            f'Environment variable "{env_var_name}" is NOT set')

SQLSERVER_BASE = None
if all(item in globals() for item in ENV_VAR_NAMES):
    # pylint:disable=undefined-variable
    SQLSERVER_BASE = f"mssql+pymssql://{SQLSERVER_USER}:{
        SQLSERVER_PWD}@{SQLSERVER_SERVER}"


@dataclasses.dataclass
class DbConfig():
    """All DB config params"""
    SQLALCHEMY_BINDS = {
        'sqlserver_latam_ar': f"{SQLSERVER_BASE}/{SQLSERVER_LATAM_AR_DB}",  # pylint:disable=undefined-variable
        'sqlserver_latam_ar_dev': f"{SQLSERVER_BASE}/{SQLSERVER_LATAM_AR_DEV_DB}",  # pylint:disable=undefined-variable
        'sqlserver_latam_ar_farmadb': f"{SQLSERVER_BASE}/{SQLSERVER_LATAM_AR_FARMADB_DB}",  # pylint:disable=undefined-variable
        'sqlserver_latam_ar_sand': f"{SQLSERVER_BASE}/{SQLSERVER_LATAM_AR_SAND_DB}",  # pylint:disable=undefined-variable
        'sqlserver_latam_ar_staging': f"{SQLSERVER_BASE}/{SQLSERVER_LATAM_AR_STAGING_DB}",  # pylint:disable=undefined-variable
        'sqlserver_latam_uy': f"{SQLSERVER_BASE}/{SQLSERVER_LATAM_UY_DB}",  # pylint:disable=undefined-variable
        'sqlserver_latam_uy_staging': f"{SQLSERVER_BASE}/{SQLSERVER_LATAM_UY_STAGING_DB}",  # pylint:disable=undefined-variable
        'godw': f"oracle+oracledb://{GODW_USER}:{GODW_PASSWORD}@{GODW_SERVER}:{GODW_PORT}/?service_name={GODW_SERVICENAME}",  # pylint:disable=undefined-variable
        'sapdwp06': f"hana+hdbcli://{SAPDWP06_USER}:{SAPDWP06_PASSWORD}@{SAPDWP06_SERVER}:{SAPDWP06_PORT}/{SAPDWP06_DB}?encrypt=true",  # pylint:disable=undefined-variable
        'rexis_sales': f"mssql+pymssql://@{REXIS_SALES_SERVER}/{REXIS_SALES_DB}",  # pylint:disable=undefined-variable
        'rexis_services': f"mssql+pymssql://@{REXIS_SERVICES_SERVER}/{REXIS_SERVICES_DB}"  # pylint:disable=undefined-variable
    }

    @classmethod
    def __get_bind__(cls, bind: str = ''):
        return cls.SQLALCHEMY_BINDS[cls.validate_bind(bind)]

    @classmethod
    def validate_bind(cls, bind: str = ''):
        """Bind validation"""
        if bind in cls.SQLALCHEMY_BINDS:
            return bind
        available_binds = ', '.join(
            f"{key}" for key in cls.SQLALCHEMY_BINDS)
        raise ValueError(
            f'Bind Key "{bind}" NOT valid. Available binds are: {available_binds}')

    @classmethod
    def test_bind(cls, bind: str = ''):
        """Bind testing. Return True if connection success, otherwise return False"""
        try:
            engine = create_engine(cls.__get_bind__(bind), echo=True)
            with engine.connect():
                return True
        except OperationalError:
            return False
        return False

    @classmethod
    def execute_query(cls, query: str, bind: str) -> List[Dict[str, Any]]:
        """Execute SQL query on specific bind and return result set as a dictionary"""
        try:
            engine = create_engine(cls.__get_bind__(bind))
            with engine.connect() as connection:
                result = connection.execute(text(query))
                # Convert query result to a dictionary
                columns = result.keys()
                rows = [dict(zip(columns, row)) for row in result.fetchall()]
                return rows
        except OperationalError as e:
            print(f"Error executing query: {e}")
            return []


DB_CONFIG = DbConfig()

# print(DB_CONFIG.execute_query('select 1+1 as c1','sqlserver_latam_ar'))
# DB_CONFIG.test_bind('rexis_services')
