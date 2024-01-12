"""DB config"""
from typing import List, Dict, Any
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
                if result.rowcount>0:
                    columns = result.keys()
                    rows = [dict(zip(columns, row)) for row in result.fetchall()]
                    return rows
        except OperationalError as e:
            print(f"Error executing query: {e}")
            return []


DB_CONFIG = DbConfig()


#class JobManager():
#    """Manager for SQL Server Agent Jobs"""
#    @classmethod
#    def __execute_query__(q: str = ''):
#        return DB_CONFIG.execute_query(q, 'sqlserver_latam_ar')
#
#    @classmethod
#    def create_python_job(cls, p_job_name: str = '', p_owner: str = '', p_path_to_bat_file: str = ''):
#        """Bind validation"""
#        # Verificar si el trabajo ya existe
#        existing_job = DB_CONFIG.execute_query(f"SELECT job_id FROM msdb.dbo.sysjobs WHERE name = '{job_name}'", 'sqlserver_latam_ar')
#        if existing_job:
#            print(existing_job)
#            input()
#            # Si el trabajo ya existe, actualizar el comando del paso 1
#            DB_CONFIG.execute_query(f"EXEC msdb.dbo.sp_update_jobstep @job_id = '{existing_job[0]["job_id"]}', @step_name = 'Execute run_app.bat', @command = '{command}'", 'sqlserver_latam_ar')
#        else:
#            # Si el trabajo no existe, crear el trabajo desde cero
#            DB_CONFIG.execute_query("EXEC msdb.dbo.sp_add_job @job_name=N'SQL_CREATED'", 'sqlserver_latam_ar')
#            #DB_CONFIG.execute_query(f"USE [msdb] EXEC msdb.dbo.sp_add_job @job_name='{p_job_name}', @enabled=1, @owner_login_name=N'{p_owner}'", 'sqlserver_latam_ar')
#            #DB_CONFIG.execute_query(f"EXEC msdb.dbo.sp_add_jobstep @job_id = @@identity, @step_name = 'Execute run_app.bat', @command = '{command}'", 'sqlserver_latam_ar')
#
#
## Configuración del trabajo y paso
#job_name = 'SQL_CREATED4'
#owner='RNUMDMAS\\digitaa2'
#command = 'cmd.exe /c "otra_ruta\run_app.bat"'
#
#
#DB_CONFIG.execute_query("EXEC msdb.dbo.sp_add_job @job_name=N'SQL_CREATED'", 'sqlserver_latam_ar')
# print(DB_CONFIG.execute_query('select 1+1 as c1','sqlserver_latam_ar'))
# DB_CONFIG.test_bind('rexis_services')
