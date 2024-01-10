from airflow.hooks.base_hook import BaseHook
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator

def task_failed_slack_alert(context, slack_conn_id='slack_default', message=None):
    """
    Sends message to Slack about task failure.

    :param context: The execution context
    :type context: dict
    :param slack_conn_id: Slack connection ID
    :type slack_conn_id: str
    :return: None

    slack_conn_id: When specifying a custom connection for a specific channel,
    ensure the the connection is created as follow:
        - host: https://hooks.slack.com/services/
        - password: <webhook_token> (rest of the hook url)
    """

    slack_webhook_token = BaseHook.get_connection(slack_conn_id).password
    
    slack_msg = """
            :red_circle: Task Failed. 
            *Task*: {task}  
            *Dag*: {dag} 
            *Configuration*: {conf}
            *Message*: {message}
            *Execution Time*: {exec_date}  
            *Log Url*: {log_url} 
            """.format(
            task=context.get('task_instance').task_id,
            dag=context.get('task_instance').dag_id,
            ti=context.get('task_instance'),
            conf=context.get('dag_run').conf,
            exec_date=context.get('execution_date'),
            log_url=context.get('task_instance').log_url,
            message=message
        )
    
    failed_alert = SlackWebhookOperator(
        task_id='task_failed_slack_alert',
        http_conn_id=slack_conn_id,
        webhook_token=slack_webhook_token,
        message=slack_msg,
        username='airflow'
    )
    return failed_alert.execute(context=context)

def task_success_slack_alert(context, slack_conn_id='slack_default', message=None):
    """
    Sends message to Slack about task success.

    :param context: The execution context
    :type context: dict
    :param slack_conn_id: Slack connection ID
    :type slack_conn_id: str
    :return: None

    slack_conn_id: When specifying a custom connection for a specific channel,
    ensure the the connection is created as follow:
        - host: https://hooks.slack.com/services/
        - password: <webhook_token> (rest of the hook url)
    """

    slack_webhook_token = BaseHook.get_connection(slack_conn_id).password
    
    slack_msg = """
            :white_check_mark: Task Success. 
            *Task*: {task}  
            *Dag*: {dag} 
            *Configuration*: {conf}
            *Message*: {message}
            *Execution Time*: {exec_date}  
            *Log Url*: {log_url} 
            """.format(
            task=context.get('task_instance').task_id,
            dag=context.get('task_instance').dag_id,
            ti=context.get('task_instance'),
            conf=context.get('dag_run').conf,
            exec_date=context.get('execution_date'),
            log_url=context.get('task_instance').log_url,
            message=message
        )
    
    success_alert = SlackWebhookOperator(
        task_id='task_success_slack_alert',
        http_conn_id=slack_conn_id,
        webhook_token=slack_webhook_token,
        message=slack_msg,
        username='airflow'
    )
    return success_alert.execute(context=context)

def task_warning_slack_alert(context, slack_conn_id='slack_default', message=None):
    """
    Sends message to Slack about task warning.

    :param context: The execution context
    :type context: dict
    :param slack_conn_id: Slack connection ID
    :type slack_conn_id: str
    :return: None

    slack_conn_id: When specifying a custom connection for a specific channel,
    ensure the the connection is created as follow:
        - host: https://hooks.slack.com/services/
        - password: <webhook_token> (rest of the hook url)
    """

    slack_webhook_token = BaseHook.get_connection(slack_conn_id).password
    
    slack_msg = """
            :warning: Task Warning. 
            *Task*: {task}  
            *Dag*: {dag} 
            *Configuration*: {conf}
            *Message*: {message}
            *Execution Time*: {exec_date}  
            *Log Url*: {log_url} 
            """.format(
            task=context.get('task_instance').task_id,
            dag=context.get('task_instance').dag_id,
            ti=context.get('task_instance'),
            conf=context.get('dag_run').conf,
            exec_date=context.get('execution_date'),
            log_url=context.get('task_instance').log_url,
            message=message
        )
    
    warning_alert = SlackWebhookOperator(
        task_id='task_warning_slack_alert',
        http_conn_id=slack_conn_id,
        webhook_token=slack_webhook_token,
        message=slack_msg,
        username='airflow'
    )
    return warning_alert.execute(context=context)