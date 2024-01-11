from evalml.automl.automl_search import AutoMLSearch as __AutoMLSearch


class Modeling1(__AutoMLSearch):
    def __init__(
        self,
        X_train=None,
        y_train=None,
        X_holdout=None,
        y_holdout=None,
        problem_type=None,
        objective="auto",
        max_iterations=None,
        max_time=None,
        patience=None,
        tolerance=None,
        data_splitter=None,
        allowed_component_graphs=None,
        allowed_model_families=None,
        features=None,
        start_iteration_callback=None,
        add_result_callback=None,
        error_callback=None,
        additional_objectives=None,
        alternate_thresholding_objective="F1",
        random_seed=0,
        n_jobs=-1,
        tuner_class=None,
        optimize_thresholds=True,
        ensembling=False,
        max_batches=None,
        problem_configuration=None,
        train_best_pipeline=True,
        search_parameters=None,
        sampler_method="auto",
        sampler_balanced_ratio=0.25,
        allow_long_running_models=False,
        _pipelines_per_batch=5,
        automl_algorithm="default",
        engine="sequential",
        verbose=False,
        timing=False,
        exclude_featurizers=None,
        holdout_set_size=0,
    ):
        super().__init__(
            X_train,
            y_train,
            X_holdout,
            y_holdout,
            problem_type,
            objective,
            max_iterations,
            max_time,
            patience,
            tolerance,
            data_splitter,
            allowed_component_graphs,
            allowed_model_families,
            features,
            start_iteration_callback,
            add_result_callback,
            error_callback,
            additional_objectives,
            alternate_thresholding_objective,
            random_seed,
            n_jobs,
            tuner_class,
            optimize_thresholds,
            ensembling,
            max_batches,
            problem_configuration,
            train_best_pipeline,
            search_parameters,
            sampler_method,
            sampler_balanced_ratio,
            allow_long_running_models,
            _pipelines_per_batch,
            automl_algorithm,
            engine,
            verbose,
            timing,
            exclude_featurizers,
            holdout_set_size,
        )

class Modeling2:
    import cloudpickle

    from evalml.automl.automl_search import AutoMLSearch

    __automl: AutoMLSearch

    @staticmethod
    def load(file_path: str):
        """Loads Modeling object at file path.

        Args:
            file_path (str): Location to find file to load

        Returns:
            Modeling object
        """

        from evalml.automl.automl_search import AutoMLSearch

        modeling = Modeling()

        modeling.__automl = AutoMLSearch.load(file_path)

        return modeling

    def save(self, file_path, pickle_type="cloudpickle", pickle_protocol=cloudpickle.DEFAULT_PROTOCOL):
        """Saves Modeling object at file path.

        Args:
            file_path (str): Location to save file.
            pickle_type ({"pickle", "cloudpickle"}): The pickling library to use.
            pickle_protocol (int): The pickle data stream format.

        Raises:
            ValueError: If pickle_type is not "pickle" or "cloudpickle".
        """

        self.__automl.save(file_path, pickle_type, pickle_protocol)

    def make_prediction(self, datasetToPredict, threshold=None):
        """Genera predicciones y retorna un dataframe con los resultados"""
        pass

    def compute_explanation(self, max_expl=5):
        """Calcula las explanations"""
        pass

    def get_model_list(self):
        """Retorna todos los proyectos existentes asociados a una cuenta"""
        pass

    def get_recommended_model_name(self, project_id):
        """Retorna el modelo recomendado de un proyecto"""
        pass

    def get_recommended_model_instance(self, project_id):
        """Retorna el objeto de un modelo recomendado de un proyecto"""
        pass

    def get_prediction_server(self):
        """Retorna el objeto con la URL asociada al servidor de predicciones"""
        pass

    def get_list_all_models_by_date(self, project):
        """Retorna la lista de todos los modelos asociados a un proyecto ordenados por fecha"""
        pass

    def get_list_all_models(self, project):
        """Retorna la lista de todos los modelos asociados a un proyecto"""
        pass

    def get_first_model_of_project(self, project):
        """Retorna el primer proyecto de la lista (útil cuando no existe un proyecto recomendado)"""
        pass

    def start_project_and_get_the_best_model(self, project_name, dataset, target, n_workers, mode="FULL_AUTO", blueprint_name=""):
        """Inicia proyecto con nuevo entrenamiento"""
        pass

    def get_best_f1_threshold(self, partition="validation"):
        """Retorna el mejor umbral asociado a la métrica F1"""
        pass

    def estimate_threshold(self, m="f1_score", partition="validation"):
        """Realiza la estimación del threshold post-entrenamiento"""
        pass

    def get_metrics(self, nameMetrics="Accuracy", partition="crossValidation"):
        """Retornas las métricas disponibles para una partición"""
        pass

    def show_all_metrics(self):
        """Retornas todas las métricas disponibles para un modelo"""
        pass

    def create_new_deployment(self, model_id, label, pred_server_id, enable_monitoring=False, description=""):
        """Crea un nuevo deployment de un modelo"""
        pass

    def get_deployment_list(self):
        """Retorna una lista con todos los deployment"""
        pass

    def get_deployment_by_label(self, label):
        """Retorna el objeto asociado al deployment por el nombre"""
        pass

    def get_deployment_by_id(self, d_id):
        """Retorna un deploiment por el id"""
        pass

    def update_deployment_label_by_id(self, d_id, new_label):
        """Actualiza el nombre de un deployment"""
        pass

    def delete_deployment_by_id(self, d_id):
        """Elimina un deployment"""
        pass

    def enable_drift_and_data_collection(self, deployment):
        """Habilita las opciones principales de seguimiento de la salud del modelo"""
        pass

    def enable_association_id(self, deployment, assoc_id):
        """Habilita la asociación de id"""
        pass

    def upload_actuals(self, deployment, actuals_df):
        """Carga el archivo con las predicciones actuales para calcular el accuracy sobre el tiempo"""
        pass

    def check_deployment_settings(self, deployment):
        """Imprime el estado de las configuraciones"""
        pass

    def replace_model_deployed(self, deployment, new_model_id, reason):
        """Reemplazo de un modelo"""
        pass

    def validate_replacement(self, deployment, model_id):
        """Valida que coincidan todos los parámetros entre el modelo actual y el que nuevo antes de reemplazar"""
        pass

    def deployment_predict(self, deployment_id, data, output_file="out.csv"):
        """Realiza predicciones mediante el deploy"""
        pass

    def create_new_ts_project_and_get_the_best_model(self, **kwargs):
        """Crea un nuevo proyecto de TS, lo configura, entrena y retorna el modelo recomendado"""
        pass

    def unlock_holdout(self, proj, best_model):
        """Desbloquea el holdout y reentrena"""
        pass

    def make_ts_prediction(self, project, model, data, last_train_date):
        """Realiza predicciones al modelo recomendado por la serie de tiempo"""
        pass

    def calc_accuracy(self, project, model_id, metric=None, n=0):
        """Calcula la precisión de cada serie para un proyecto multi-serie"""
        pass

    def get_model_sorted_by_best_accuracy(self, project):
        """Retorna una lista del leaderboard ordenado por el mejor accuracy (MASE)"""
        pass

    def getKwargs(self, args, kwargs):
        """Retorna un diccionario con las variables recibidas por parámetro"""
        pass

    def _print(self, to_console):
        """Imprime el log por pantalla si está activo"""
        pass


# Cargar
# Entrenar
# Predecir
# Listar modelos
# Escoger mejor modelo
# Guardar
