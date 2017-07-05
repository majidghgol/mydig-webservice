from manage_oozie_jobs import OozieJobs
from manage_workflow_xml import WM


class SubmitEtk(object):
    def __init__(self):
        # http://10.1.94.54:14000/webhdfs/v1?user.name=aglahe&op=LISTSTATUS
        # https://webhdfs.memexproxy.com/webhdfs/v1?user.name=aglahe&op=LISTSTATUS
        self.web_hdfs_url = "http://10.1.94.54:14000/webhdfs/v1?user.name={}"
        self.oozie_url = "http://10.1.94.54:11000/oozie"
        self.worker_dir_path = '/user/worker/etk'
        self.default_lib_path = '{}/{}/lib/{}'
        self.files_to_upload = dict()

    @staticmethod
    def get_file_name_from_path(file_path):
        v = file_path.split('/')
        return v[len(v) - 1].strip()

    def add_things_to_upload(self, key, source, destination):
        self.files_to_upload[key] = dict()
        self.files_to_upload[key]['source'] = source
        self.files_to_upload[key]['destination'] = destination

    def create_worflow_xml(self, etk_config, project_name, workflow_manager):
        # Add arguments for etk
        arguments = ['{INPUT}', '{OUTPUT}', 'extraction_config.json']
        argument_xml = ''
        for argument in arguments:
            argument_xml += workflow_manager.create_arguments_for_workflow_xml(argument)

        # read etk and add all the files to workflow xml
        files = ''
        if 'resources' in etk_config:
            if 'dictionaries' in etk_config['resources']:
                dictionaries = etk_config['resources']['dictionaries']
                for k, v in dictionaries.items():
                    f = self.default_lib_path.format(self.worker_dir_path, project_name, self.get_file_name_from_path(v))
                    files += workflow_manager.create_file_property_for_workflow_xml(f)
                    self.add_things_to_upload(k, v, f)
            if 'landmark' in etk_config['resources']:
                landmark = etk_config['resources']['landmark']
                if len(landmark) > 0:
                    landmark_f = landmark[0]
                    f = self.default_lib_path.format(self.worker_dir_path, project_name,
                                                     self.get_file_name_from_path(landmark_f))
                    files += workflow_manager.create_file_property_for_workflow_xml(f)
                    self.add_things_to_upload('landmark', landmark_f, f)
            if 'spacy_field_rules' in etk_config['resources']:
                spacy_field_rules = etk_config['resources']
                for k, v in spacy_field_rules.items():
                    f = self.default_lib_path.format(self.worker_dir_path, project_name,
                                                     self.get_file_name_from_path(v))
                    files += workflow_manager.create_file_property_for_workflow_xml(f)
                    self.add_things_to_upload(k, v, f)

        # add some defaults to files
        """
        <file>/user/worker/etk/lib/run_etk_spark.py#run_etk_spark.py</file>
            <file>/user/worker/etk/lib/etk_env.zip#etk_env.zip</file>
            <file>/user/worker/etk/lib/python-lib.zip#python-lib.zip</file>
            <file>/user/worker/etk/lib/run.sh#run.sh</file>
            <file>/user/worker/etk/lib/pyspark#pyspark</file>
        """
        files += workflow_manager.create_file_property_for_workflow_xml('{}/lib/etk_env.zip'.format(self.worker_dir_path))

        # put everything else in project's lib
        def_fs = ['run_etk_spark.py', 'python-lib.zip', 'run.sh', 'pyspark' ]
        for def_f in def_fs:
            if def_f == 'run.sh':
                self.add_things_to_upload('run.sh', 'run.sh', self.default_lib_path.format(self.worker_dir_path, project_name, def_f))
            files += workflow_manager.create_file_property_for_workflow_xml(
                self.default_lib_path.format(self.worker_dir_path, project_name, def_f))

        # add the etk env, this should be pretty constant and wouldn't have to be updated
        archive = workflow_manager.create_archive_property_for_workflow_xml('{}/lib/etk_env.zip'.format(self.worker_dir_path))

        return '{}{}{}{}{}'.format(workflow_manager.workflow_xml_start, argument_xml, files, archive, workflow_manager.workflow_xml_end)

    def update_etk_lib_cluster(self, master_project_config, project_name):
        # TODO upload the dicts and other resources to cluster

        # TODO update the workflow.xml and upload to the /user/worker/summer_evaluation_2017/workflows/etk/

        # TODO update run.sh and upload to cluster

        return

    def submit_etk_cluster(self, master_project_config, project_name):
        property_dict = dict()
        property_dict["user.name"] = "asingh"
        property_dict[
            "oozie.wf.application.path"] = "hdfs://memex:8020/user/worker/summer_evaluation_2017/workflows/etk/"
        property_dict["jobTracker"] = "memex-rm.xdata.data-tactics-corp.com:8032"
        property_dict["nameNode"] = "hdfs://memex"
        property_dict["oozie.use.system.libpath"] = "True"
        property_dict['INPUT'] = '/user/worker/summer_evaluation_2017/{}/es/full'.format(project_name)
        current_version = master_project_config['index']['version']
        property_dict['OUTPUT'] = '/user/worker/summer_evaluation_2017/{}/etk_out/{}'.format(project_name, str(current_version))
        oj = OozieJobs(oozie_url=self.oozie_url)
        oj.submit_oozie_jobs(property_dict)

if __name__ == '__main__':
    etk_config = '/Users/amandeep/Downloads/extraction_config_rqs.json'
    s = SubmitEtk()
    import json, codecs
    wm  = WM()
    print s.create_worflow_xml(json.load(codecs.open(etk_config)), 'pedro_test_01', wm)