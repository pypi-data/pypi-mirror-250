import json
import os.path
from typing import Dict

from steam_sdk.analyses.AnalysisSTEAM import AnalysisSTEAM
from steam_sdk.builders.BuilderModel import BuilderModel
from steam_sdk.data.DataAnalysis import MakeModel, ModifyModelMultipleVariables, SetUpFolder
from steam_sdk.data.DataModelCosim import DataModelCosim, sim_LEDET, sim_PSPICE
from steam_sdk.utils.delete_if_existing import delete_if_existing
from steam_sdk.utils.make_folder_if_not_existing import make_folder_if_not_existing


class ParserCOSIM:
    """
        Class with methods to read/write COSIM information from/to other programs
    """

    def __init__(self, builder_model: BuilderModel = BuilderModel(flag_build=False), #TODO remove if not needed relative_path_settings: str = '',
                 temp_output_path: str = 'temp'):
        '''
        Initialization using a BuilderModel object containing COSIM parameter structure
        :param builder_model: BuilderModel object containing COSIM parameter structure
        :param relative_path_settings: Path to the file defining the STEAM settings
        '''

        # Load co-simulation data from the BuilderModel object
        self.cosim_data: DataModelCosim = builder_model.cosim_data

        # Assign input
        # self.relative_path_settings = relative_path_settings
        self.temp_output_path = temp_output_path

    def write_cosim_model(self, verbose: bool = False):
        self.setup_cosim_folders(verbose=verbose)
        self.write_config_file(verbose=verbose)
        for model_name, model in self.cosim_data.Simulations.items():
            if verbose: (f'{model_name}, {model}')
            if model.type == 'FiQuS':
                self.write_model_FiQuS(model_name=model_name, model=model, verbose=verbose)
            elif model.type == 'LEDET':
                self.write_model_LEDET(model_name=model_name, model=model, verbose=verbose)
            elif model.type == 'PSPICE':
                self.write_model_PSPICE(model_name=model_name, model=model, verbose=verbose)
            elif model.type == 'XYCE':
                self.write_model_XYCE(model_name=model_name, model=model, verbose=verbose)


    def write_config_file(self, output_file_name: str = 'COSIMConfig.json', verbose: bool = False):
        '''
        ** Write COSIM configuration file **
        '''

        # Unpack input
        local_COSIM_folder = self.cosim_data.Folders.local_COSIM_folder
        cosim_name = self.cosim_data.GeneralParameters.cosim_name
        sim_number = str(self.cosim_data.GeneralParameters.simulation_number)

        # Calculate variables
        coSimulationDir = self.reformat_path(os.path.join(local_COSIM_folder, cosim_name, sim_number, 'Output')) + '\\'
        t_0 = self.cosim_data.Settings.Time_Windows.t_0
        t_end = self.cosim_data.Settings.Time_Windows.t_end
        executionOrder = self.cosim_data.Settings.Options_run.executionOrder
        executeCleanRun = self.cosim_data.Settings.Options_run.executeCleanRun
        coSimulationModelSolvers, coSimulationModelDirs, coSimulationModelConfigs, coSimulationPortDefinitions = [], [], [], []
        convergenceVariables, relTolerance, absTolerance, t_step_max = [], [], [], []
        for model_name, model in self.cosim_data.Simulations.items():
            coSimulationModelSolvers.append(model.type)
            coSimulationModelDirs.append(self.reformat_path(os.path.join(local_COSIM_folder, cosim_name, sim_number, 'Input', model_name)) + '\\')
            coSimulationModelConfigs.append(f'{model_name}_config.json')
            coSimulationPortDefinitions.append(f'{model_name}_InputOutputPortDefinition.json')
            convergenceVariables.append(self.cosim_data.Settings.Convergence.convergenceVariables[model_name])
            relTolerance.append(self.cosim_data.Settings.Convergence.relTolerance[model_name])
            absTolerance.append(self.cosim_data.Settings.Convergence.absTolerance[model_name])
            t_step_max.append(self.cosim_data.Settings.Time_Windows.t_step_max[model_name])

        # Dictionary to write
        dict_cosim_config = {
                "coSimulationDir": coSimulationDir,
                "coSimulationModelSolvers": coSimulationModelSolvers,
                "coSimulationModelDirs": coSimulationModelDirs,
                "coSimulationModelConfigs": coSimulationModelConfigs,
                "coSimulationPortDefinitions": coSimulationPortDefinitions,
                "convergenceVariables": convergenceVariables,
                "t_0": t_0,
                "t_end": t_end,
                "t_step_max": t_step_max,
                "relTolerance": relTolerance,
                "absTolerance": absTolerance,
                "executionOrder": executionOrder,
                "executeCleanRun": executeCleanRun
        }

        # Serializing json
        json_cosim_config = json.dumps(dict_cosim_config, indent=4)

        # Writing to .json file
        path_output_file = os.path.join(local_COSIM_folder, cosim_name, sim_number, 'Input', output_file_name)
        make_folder_if_not_existing(os.path.dirname(path_output_file), verbose=verbose)
        with open(path_output_file, "w") as outfile:
            outfile.write(json_cosim_config)
        if verbose:
            print(f'File {path_output_file} written.')


    def setup_cosim_folders(self, verbose: bool = False):
        '''
        ** Setup COSIM folder and subfolders **
        '''
        # Unpack input
        local_COSIM_folder = self.cosim_data.Folders.local_COSIM_folder
        cosim_name = self.cosim_data.GeneralParameters.cosim_name
        sim_number = str(self.cosim_data.GeneralParameters.simulation_number)

        path_model_folder = os.path.join(local_COSIM_folder, cosim_name, sim_number, 'Input')
        make_folder_if_not_existing(path_model_folder, verbose=verbose)
        for model_name, model in self.cosim_data.Simulations.items():
            path_submodel_folder = os.path.join(path_model_folder, model_name)
            make_folder_if_not_existing(path_submodel_folder, verbose=verbose)


    def write_model_FiQuS(self, model_name: str, model, verbose: bool = False):
        '''
        ** Write selected FiQuS model **
        '''
        # Make subfolders
        # TODO
        pass

    def write_model_LEDET(self, model_name: str, model, verbose: bool = False):
        '''
        ** Write selected LEDET model **
        '''
        # Unpack input
        local_COSIM_folder = self.cosim_data.Folders.local_COSIM_folder
        cosim_name = self.cosim_data.GeneralParameters.cosim_name
        sim_number = str(self.cosim_data.GeneralParameters.simulation_number)
        magnet_name = model.modelName
        solverPath = self.reformat_path(model.solverPath)

        # Make subfolders
        path_submodel_folder = os.path.join(local_COSIM_folder, cosim_name, sim_number, 'Input', model_name)
        make_folder_if_not_existing(path_submodel_folder, verbose=verbose)
        make_folder_if_not_existing(os.path.join(path_submodel_folder, 'LEDET', magnet_name, 'Input'), verbose=verbose)
        make_folder_if_not_existing(os.path.join(path_submodel_folder, 'LEDET', magnet_name, 'Input', 'Control current input'), verbose=verbose)
        make_folder_if_not_existing(os.path.join(path_submodel_folder, 'LEDET', magnet_name, 'Input', 'Initialize variables'), verbose=verbose)
        make_folder_if_not_existing(os.path.join(path_submodel_folder, 'Field maps', magnet_name), verbose=verbose)
        # Make configuration file
        path_config_file = os.path.join(path_submodel_folder, f'{model_name}_config.json')
        self.write_config_file_ledet(output_file=path_config_file, LEDET_path=solverPath, magnet_name=magnet_name, sim_set_number=model.simulationNumber)
        # Make input/output port definition file
        path_ports_file = os.path.join(path_submodel_folder, f'{model_name}_InputOutputPortDefinition.json')
        self.write_ports_file(output_file=path_ports_file, model_name=model_name)
        # Make input files, self-mutual inductance files, magnetic field map files. Save them to the COSIM subfolder. Delete temporary files.
        self.make_input_files_ledet(model_name=model_name, model=model, verbose=verbose)

    def write_model_PSPICE(self, model_name: str, model, verbose: bool = False):
        '''
        ** Write selected PSPICE model **
        '''
        # Unpack input
        local_COSIM_folder = self.cosim_data.Folders.local_COSIM_folder
        cosim_name = self.cosim_data.GeneralParameters.cosim_name
        sim_number = str(self.cosim_data.GeneralParameters.simulation_number)
        model_library_folder = model.modelFolder
        magnet_name = model.modelName

        # Make subfolders
        path_submodel_folder = os.path.join(local_COSIM_folder, cosim_name, sim_number, 'Input', model_name)
        make_folder_if_not_existing(path_submodel_folder, verbose=verbose)
        # Make configuration file
        path_config_file = os.path.join(path_submodel_folder, f'{model_name}_config.json')
        self.write_config_file_pspice(output_file=path_config_file, model=model)
        # Make input/output port definition file
        path_ports_file = os.path.join(path_submodel_folder, f'{model_name}_InputOutputPortDefinition.json')
        self.write_ports_file(output_file=path_ports_file, model_name=model_name)
        # Make input netlist file
        # Copy input netlist file
        # Copy auxiliary files
        # Delete temporary files
        pass  # TODO

    def write_model_XYCE(self, model_name: str, model, verbose: bool = False):
        '''
        ** Write selected XYCE model **
        '''
        # Make subfolders
        # Make configuration file
        # Make input/output port definition file
        # Make input netlist file
        # Copy input netlist file
        # Copy auxiliary files
        # Delete temporary files
        pass  # TODO


    @staticmethod
    def reformat_path(path: str):
        '''
        Reformat a string defining a path so that all delimiters are double slashes
        :param path: string defining the original path
        :return: str
        '''

        return os.path.normpath(path).replace(os.sep, '\\')

    @staticmethod
    def write_config_file_ledet(output_file: str, LEDET_path: str, magnet_name: str, sim_set_number: int):
        '''
        Write the LEDET configuration .json file
        :param output_file: Target file
        :param LEDET_path: Path to PSPICE executable
        :param sim_set_number: Number of the simulation set, i.e. number of the LEDET simulation used in the COSIM model
        :return: None
        '''

        # Dictionary to write
        dict_ledet_config = {
            "solverPath": f"{LEDET_path}",
            "modelFolder": "LEDET",
            "modelName": f"{magnet_name}",
            "simulationNumber": f"{sim_set_number}"
        }

        # Serializing json
        json_ledet_config = json.dumps(dict_ledet_config, indent=4)

        # Writing to .json file
        with open(output_file, "w") as outfile:
            outfile.write(json_ledet_config)

    @staticmethod
    def write_config_file_pspice(output_file: str, model: sim_PSPICE):
        '''
        Write the PSPICE configuration .json file
        :param output_file: Target file
        :param model: sim_PSPICE object containing the information about this model
        :return: None
        '''
        # Unpack inputs
        solverPath = ParserCOSIM.reformat_path(model.solverPath)
        modelName = model.modelName
        configurationFileName = model.configurationFileName
        externalStimulusFileName = model.externalStimulusFileName
        initial_conditions = model.initialConditions
        skipBiasPointCalculation = model.skipBiasPointCalculation

        # Write a list of initial conditions
        string_initial_conditions = [f'{ic_name}={ic}' for ic_name, ic in initial_conditions.items()]

        # Dictionary to write
        dict_pspice_config = {
            "solverPath": solverPath,
            "modelName": f'{modelName}.cir',
            "configurationFileName": configurationFileName,
            "externalStimulusFileName": externalStimulusFileName,
            "initialConditions": string_initial_conditions,
            "skipBiasPointCalculation": skipBiasPointCalculation,
        }

        # Serializing json
        json_pspice_config = json.dumps(dict_pspice_config, indent=4)

        # Writing to .json file
        with open(output_file, "w") as outfile:
            outfile.write(json_pspice_config)

    def write_ports_file(self, output_file: str, model_name: str):
        '''
            Write the input/output port configuration .json file
            :param output_file: Target file
            :return: None
        '''

        list_of_dict_ports = []
        for port_name, port in self.cosim_data.PortDefinition.items():
            if model_name in port.Models:
                port_info = port.Models[model_name]

                # Dictionary to write
                dict_ports = {
                    "name": port_name,
                    "components": port_info.components,
                    "inputs": [],
                    "outputs": [],
                }
                for input_name, input in port_info.inputs.items():
                    dict_ports["inputs"].append({
                        "couplingParameter": input.variable_coupling_parameter,
                        "labels": input.variable_name,
                        "types": input.variable_type})
                for output_name, output in port_info.outputs.items():
                    dict_ports["outputs"].append({
                        "couplingParameter": output.variable_coupling_parameter,
                        "labels": output.variable_name,
                        "types": output.variable_type})
                list_of_dict_ports.append(dict_ports)

        # Writing to .json file
        with open(output_file, "w") as outfile:
            # Serializing json
            for dict_ports in list_of_dict_ports:
                json_ports = json.dumps(dict_ports, indent=4)
                outfile.write(json_ports)
                outfile.write('\n')


    def make_input_files_ledet(self, model_name: str, model: sim_LEDET, verbose: bool = False):
        # Hard-coded variables
        software = 'LEDET'
        dummy_model_name = 'MODEL_NAME'  # This name is not important

        # Unpack input
        local_COSIM_folder = self.cosim_data.Folders.local_COSIM_folder
        cosim_name = self.cosim_data.GeneralParameters.cosim_name
        sim_number = str(self.cosim_data.GeneralParameters.simulation_number)

        # Delete temporary output folder, if present
        delete_if_existing(self.temp_output_path, verbose=verbose)

        # Initialize STEAM analysis object
        aSTEAM = AnalysisSTEAM(file_name_analysis=None, verbose=verbose)
        # Define model folder as the current subfolder in the COSIM model
        aSTEAM.data_analysis.GeneralParameters.flag_permanent_settings = True  # This will make sure all settings are defined in this code
        aSTEAM.data_analysis.PermanentSettings.local_LEDET_folder = os.path.join(local_COSIM_folder, cosim_name, sim_number, 'Input', model_name, 'LEDET')
        aSTEAM._load_and_write_settings(relative_path_settings='')
        # Define folder paths
        aSTEAM.data_analysis.WorkingFolders.library_path = model.modelFolder  # TODO: maybe the following key should be deleted: self.cosim_data.Folders.path_model_folder
        aSTEAM.data_analysis.WorkingFolders.output_path = self.temp_output_path
        aSTEAM.data_analysis.WorkingFolders.temp_path = 'TO_IGNORE'  # This dummy value is not used
        aSTEAM._set_up_working_folders()
        # Initialize the simulation steps
        aSTEAM.data_analysis.AnalysisStepDefinition = {}
        # Add step to setup model folder
        step_setup_folder = f'setupFolder'
        aSTEAM.data_analysis.AnalysisStepDefinition[step_setup_folder] = SetUpFolder(type='SetUpFolder')
        aSTEAM.data_analysis.AnalysisStepDefinition[step_setup_folder].software = [software]
        aSTEAM.data_analysis.AnalysisStepDefinition[step_setup_folder].simulation_name = model.modelName
        # Add step to make model
        step_make_model = f'makeModel'
        aSTEAM.data_analysis.AnalysisStepDefinition[step_make_model] = MakeModel(type='MakeModel')
        aSTEAM.data_analysis.AnalysisStepDefinition[step_make_model].model_name = dummy_model_name
        aSTEAM.data_analysis.AnalysisStepDefinition[step_make_model].file_model_data = model.modelName
        aSTEAM.data_analysis.AnalysisStepDefinition[step_make_model].case_model = model.modelCase
        aSTEAM.data_analysis.AnalysisStepDefinition[step_make_model].flag_build = True
        aSTEAM.data_analysis.AnalysisStepDefinition[step_make_model].software = [software]
        # Add step to modify selected variables
        step_modify_model = f'modifyModelParameters'
        aSTEAM.data_analysis.AnalysisStepDefinition[step_modify_model] = ModifyModelMultipleVariables(type='ModifyModelMultipleVariables')
        aSTEAM.data_analysis.AnalysisStepDefinition[step_modify_model].model_name = dummy_model_name
        aSTEAM.data_analysis.AnalysisStepDefinition[step_modify_model].variables_to_change = model.variables_to_modify.variables_to_change
        aSTEAM.data_analysis.AnalysisStepDefinition[step_modify_model].variables_value = model.variables_to_modify.variables_values
        aSTEAM.data_analysis.AnalysisStepDefinition[step_modify_model].software = [software]
        # Add step to make sure the input file are generated with the correct simulation number (this is done by assigning a dummy variable modification)
        step_write_model = f'writeModel'
        aSTEAM.data_analysis.AnalysisStepDefinition[step_write_model] = ModifyModelMultipleVariables(type='ModifyModelMultipleVariables')
        aSTEAM.data_analysis.AnalysisStepDefinition[step_write_model].model_name = dummy_model_name
        aSTEAM.data_analysis.AnalysisStepDefinition[step_write_model].variables_to_change = ['GeneralParameters.model.name']
        aSTEAM.data_analysis.AnalysisStepDefinition[step_write_model].variables_value = [[model_name]]
        aSTEAM.data_analysis.AnalysisStepDefinition[step_write_model].simulation_numbers = [model.simulationNumber]
        aSTEAM.data_analysis.AnalysisStepDefinition[step_write_model].simulation_name = model.modelName
        aSTEAM.data_analysis.AnalysisStepDefinition[step_write_model].software = [software]
        # Make the list of simulation steps
        aSTEAM.data_analysis.AnalysisStepSequence = []
        aSTEAM.data_analysis.AnalysisStepSequence.append(step_setup_folder)
        aSTEAM.data_analysis.AnalysisStepSequence.append(step_make_model)
        aSTEAM.data_analysis.AnalysisStepSequence.append(step_modify_model)
        aSTEAM.data_analysis.AnalysisStepSequence.append(step_write_model)
        aSTEAM.data_analysis.AnalysisStepSequence.append(step_setup_folder)
        # Write the STEAM analysis data to a yaml file (this file works as a log file)
        path_output_file_analysis = os.path.join(self.temp_output_path, f'log_analysisSTEAM_{model_name}.yaml')
        aSTEAM.write_analysis_file(path_output_file_analysis)
        # Run analysis
        aSTEAM.run_analysis()

        # Delete temporary output folder
        delete_if_existing(self.temp_output_path, verbose=verbose)