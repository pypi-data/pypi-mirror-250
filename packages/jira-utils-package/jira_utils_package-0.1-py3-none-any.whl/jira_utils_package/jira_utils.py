# jira_utils_package/jira_utils.py
from jira import JIRA, JIRAError

class JiraUtils:
    def __init__(self, server, username, password, version, labels='自动化测试', priority=3):
        """
        使用 Jira 服务器连接初始化 JiraUtils 类。
        :param server: Jira 服务器地址
        :param username: Jira 用户名
        :param password: Jira 密码
        :param version: Jira 版本
        :param labels: Jira 标签（默认为 '自动化测试'）
        :param priority: Jira 优先级（默认为 3）
        """
        try:
            self.jira_client = JIRA(server=server, basic_auth=(username, password))
            self.version = version
            self.priority = priority
            self.labels = labels
            self.issueType = 'Bug'
        except JIRAError as e:
            print(f"初始化 Jira 客户端时出错: {e}")

    def create_issue(self, title, data_info, agent, files, project_key='SVROM'):
        """
        使用指定参数创建新的 Jira 问题单。
        :param title: 问题单标题
        :param data_info: 问题单描述
        :param agent: 问题单经办人
        :param files: 附件路径列表
        :param project_key: Jira 项目的 Key（默认为 'SVROM'）
        :return: None
        """
        try:
            new_issue = self.jira_client.create_issue(
                project=project_key,
                summary=f'{title}',
                description=f'{data_info}',
                issuetype={'name': self.issueType},
                assignee={'name': f'{agent}'},
                versions=[{"name": self.version}],
                priority={'id': self.priority},
                labels=[self.labels]
            )

            for file in files:
                # 使用 self.jira_client.add_attachment 将附件添加到新创建的问题单
                self.jira_client.add_attachment(issue=new_issue.id, attachment=file)
        except JIRAError as e:
            print(f"创建 Jira 问题单时出错: {e}")
