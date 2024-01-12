import click
import os
from typing import Tuple, List, Dict, Any, Optional
from opus.utils import common_utils
from opus import opus_logging, frameworks, clouds, jobs


logger = opus_logging.init_logger(__name__)

def list_cloud_provider(config: Optional[Dict[str, Any]]) -> None:
    table_head = [
        "NAME",
        "TYPE",
        "GROUP",
        "NODE(IDLE/TOTAL)"
    ]
    cloud_table = common_utils.create_table(table_head)

    if config:
        valid_cloud_types = [member.name.lower() for member in clouds.CloudProviders]
        for cloud_name, cloud_conf in config.get('clouds').items():
            cloud_type = cloud_conf.get('type')
            if cloud_type.lower() not in valid_cloud_types:
                click.secho(f"Invalid cloud type '{cloud_type}' for cloud '{cloud_name}'. Only {valid_cloud_types} are supported.", 
                            fg='red', nl=True)
                continue
            cloud = clouds.CloudProviders[cloud_type.upper()].value(name=cloud_name, 
                                                                    cloud_type=cloud_conf.get('type'), 
                                                                    login_node=cloud_conf.get('loginNode'))
            ok, cloud_records = cloud.get_resources_info()
            logger.debug("Check cloud name: {}".format(cloud.name))
            if ok:
                cloud_table.add_row(cloud_records)

    if len(cloud_table._rows) == 0:
        click.echo('No existing cloud resources.')
    else:
        click.echo(cloud_table)

def launch(framework: frameworks.Framework) -> None:
    logger.info("Start launching...")
    framework.launch()

def framework_list(status: Tuple[str], cloud_providers: Tuple[str]) -> List[List[str]]:
    # Update frameworks status first.
    framework_records = frameworks.Framework.get_frameworks(
        [[('status', s) for s in frameworks.FrameworkStatus.unstopped()]]
    )
    for record in framework_records:
        framework = frameworks.FrameworkType[record['framework_type'].upper()].value
        framework = framework.create_from_record(record)
        framework.get_status()

    # List Framework
    filter_options = []
    filter_options = [[('status', s.upper()) for s in status]] if status else []
    filter_options += [[('cloud', 'cloud_type\": \"'+ c.lower()) for c in cloud_providers]] if cloud_providers else []
    return frameworks.Framework.get_frameworks(filter_options)

def framework_stop(framework_id: str) -> None:
    record = frameworks.Framework.get_frameworks([[('id', framework_id)]])[0]
    framework = frameworks.FrameworkType[record['framework_type'].upper()].value
    framework = framework.create_from_record(record)
    framework.stop()

def list_job(status: Tuple[str], framework_id: Tuple[int]) -> List[Dict[str, Any]]:
    filter_options = []
    if len(status) > 0:
        filter_options.append([('status', s.upper()) for s in status])
    if len(framework_id) > 0:
        filter_options.append([('framework_id', f) for f in framework_id])
    return jobs.Job.list(filter_options)


def stop_job(job: 'jobs.Job') -> None:
    if job.status == jobs.JobStatus.INIT.value:
        raise Exception('Job is initializing, it is not safe to stop it now.')
    elif job.status not in jobs.JobStatus.unfinished():
        raise Exception(f"Job was {job.status}, should not stop it again.")
    else:
        job.stop()


def download_job_logs(job: 'jobs.Job') -> str:
    log_dir = '~/opus/logs'
    log_path = os.path.join(os.path.expanduser(log_dir), f'job_{job.job_id}.log')
    os.makedirs(os.path.dirname(log_path), exist_ok = True)
    logs = job.logs(follow = False)
    with open(log_path, mode = 'w', encoding = 'utf-8') as f:
        print(logs, file = f)
    return log_path


async def follow_job_logs(job: 'jobs.Job', follow: bool) -> None:
    logs = job.logs(follow)
    async for lines in logs:
        print(lines, end = "")
    job.sync_status()
    click.secho(('\n---------------------------------------'
                 f'\n Job ended with status: {job.status}'
                 '\n---------------------------------------'), 
                 fg = 'yellow')