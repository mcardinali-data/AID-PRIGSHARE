"""
Model exported as python.
Name : AID-PRIGSHARE
Group : 
With QGIS : 32205
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Aidprigshare(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('indivualsgeolocation', 'Indivuals Geolocation', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterString('idfield', 'ID_Field (identifier to seperate individuals in individual geolocation file)', multiLine=False, defaultValue='ID'))
        self.addParameter(QgsProcessingParameterBoolean('useeuclideandistancetocalculatemeanndvi', 'Use Euclidean Distance to calculate mean Vegetation Index', optional=True, defaultValue=False))
        self.addParameter(QgsProcessingParameterBoolean('usenetworkdistancetocalculate', 'Use Network Distance to calculate (only uncheck if you only want Euclidean Distance Vegetation Index. Other green space indicators need network distance to run properly) ', defaultValue=True))
        self.addParameter(QgsProcessingParameterVectorLayer('walkabilitylayerstreetnetwork', 'Walkability Layer (Street Network)', optional=True, types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('calculatevegetationindicators', 'Calculate Vegetation Indicators', defaultValue=False))
        self.addParameter(QgsProcessingParameterVectorLayer('ndvi', 'Vegetation Index (needs to be vectorized)', optional=True, types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('calculategreenspaces', 'Calculate Green Space Indicators', defaultValue=False))
        self.addParameter(QgsProcessingParameterVectorLayer('pgs', 'Public Green Space Layer', optional=True, types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('calculatesemipublicprivategreenspaceindicators', 'Calculate semi-public & private green space indicators', defaultValue=False))
        self.addParameter(QgsProcessingParameterVectorLayer('pgs (2)', 'Semi-Public Green Spaces (will add SPGS indicator)', optional=True, types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('pgs (2) (2)', 'Private Green Space (will add PRGS indicator)', optional=True, types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('pgs (2) (3)', 'Buildings (will subtract building footprint from all green spaces if provided)', optional=True, types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('calculategreenspaceusesindicator', 'Calculate Green Space Uses Indicator', defaultValue=False))
        self.addParameter(QgsProcessingParameterVectorLayer('pgs (2) (4)', 'Green Space Use 1', optional=True, types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('pgs (2) (4) (2)', 'Green Space Use 2', optional=True, types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('pgs (2) (4) (2) (2)', 'Green Space Use 3', optional=True, types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('pgs (2) (4) (2) (2) (2)', 'Green Space Use 4', optional=True, types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('pgs (2) (4) (2) (2) (2) (2)', 'Green Space Use 5', optional=True, types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('pgs (2) (4) (2) (2) (2) (2) (2)', 'Green Space Use 6', optional=True, types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('PublicGreenSpaceWithinNetworkDistanceM2WithinBsa', 'Public Green Space within network distance (m2 within BSA)', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('NdviAroundAResidentialAdressMeanWithinBuffer', 'NDVI around a residential adress (mean within buffer)', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('NdviInNetworkDistanceMeanInBsa', 'NDVI in network distance (mean in BSA)', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('PublicGreenSpaceAccessibleWithinNetworkDistanceM2ThatIntersectWithBsa', 'Public Green Space accessible within network distance (m2 that intersect with BSA)', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('SemipublicPrivateGreenSpacesM2PerIndividual', 'Semi-Public & Private Green Spaces (m2) per Individual', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('GreenSpaceUsesWithinNetworkDistanceTotalSumAndDifferentUses', 'Green Space Uses within network distance (total sum and different uses)', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(436, model_feedback)
        results = {}
        outputs = {}

        # Calculate Green Spaces?
        alg_params = {
        }
        outputs['CalculateGreenSpaces'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Conditional branch
        alg_params = {
        }
        outputs['ConditionalBranch'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Use Network Distance?
        alg_params = {
        }
        outputs['UseNetworkDistance'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Service area (from layer)_900
        alg_params = {
            'DEFAULT_DIRECTION': 2,  # Both directions
            'DEFAULT_SPEED': 50,
            'DIRECTION_FIELD': '',
            'INCLUDE_BOUNDS': False,
            'INPUT': parameters['walkabilitylayerstreetnetwork'],
            'SPEED_FIELD': '',
            'START_POINTS': parameters['indivualsgeolocation'],
            'STRATEGY': 0,  # Shortest
            'TOLERANCE': 0,
            'TRAVEL_COST2': 900,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT_LINES': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ServiceAreaFromLayer_900'] = processing.run('native:serviceareafromlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Calculate Vegetation Index?
        alg_params = {
        }
        outputs['CalculateVegetationIndex'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Service area (from layer)_1000
        alg_params = {
            'DEFAULT_DIRECTION': 2,  # Both directions
            'DEFAULT_SPEED': 50,
            'DIRECTION_FIELD': '',
            'INCLUDE_BOUNDS': False,
            'INPUT': parameters['walkabilitylayerstreetnetwork'],
            'SPEED_FIELD': '',
            'START_POINTS': parameters['indivualsgeolocation'],
            'STRATEGY': 0,  # Shortest
            'TOLERANCE': 0,
            'TRAVEL_COST2': 1000,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT_LINES': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ServiceAreaFromLayer_1000'] = processing.run('native:serviceareafromlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Use Euclidean Distance?
        alg_params = {
        }
        outputs['UseEuclideanDistance'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # B1500
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 1500,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['indivualsgeolocation'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['B1500'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Service area (from layer)_1100
        alg_params = {
            'DEFAULT_DIRECTION': 2,  # Both directions
            'DEFAULT_SPEED': 50,
            'DIRECTION_FIELD': '',
            'INCLUDE_BOUNDS': False,
            'INPUT': parameters['walkabilitylayerstreetnetwork'],
            'SPEED_FIELD': '',
            'START_POINTS': parameters['indivualsgeolocation'],
            'STRATEGY': 0,  # Shortest
            'TOLERANCE': 0,
            'TRAVEL_COST2': 1100,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ServiceAreaFromLayer_1100'] = processing.run('native:serviceareafromlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Buffer_25_1100
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 25,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['ServiceAreaFromLayer_1100']['OUTPUT'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer_25_1100'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # B300
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 300,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['indivualsgeolocation'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['B300'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Service area (from layer)_1400
        alg_params = {
            'DEFAULT_DIRECTION': 2,  # Both directions
            'DEFAULT_SPEED': 50,
            'DIRECTION_FIELD': '',
            'INCLUDE_BOUNDS': False,
            'INPUT': parameters['walkabilitylayerstreetnetwork'],
            'SPEED_FIELD': '',
            'START_POINTS': parameters['indivualsgeolocation'],
            'STRATEGY': 0,  # Shortest
            'TOLERANCE': 0,
            'TRAVEL_COST2': 1400,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT_LINES': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ServiceAreaFromLayer_1400'] = processing.run('native:serviceareafromlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # B100
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 100,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['indivualsgeolocation'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['B100'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # NDVI_B300 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['B300']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b300JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Service area (from layer)_300
        alg_params = {
            'DEFAULT_DIRECTION': 2,  # Both directions
            'DEFAULT_SPEED': 50,
            'DIRECTION_FIELD': '',
            'INCLUDE_BOUNDS': False,
            'INPUT': parameters['walkabilitylayerstreetnetwork'],
            'SPEED_FIELD': '',
            'START_POINTS': parameters['indivualsgeolocation'],
            'STRATEGY': 0,  # Shortest
            'TOLERANCE': 0,
            'TRAVEL_COST2': 300,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT_LINES': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ServiceAreaFromLayer_300'] = processing.run('native:serviceareafromlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # B700
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 700,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['indivualsgeolocation'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['B700'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Service area (from layer)_800
        alg_params = {
            'DEFAULT_DIRECTION': 2,  # Both directions
            'DEFAULT_SPEED': 50,
            'DIRECTION_FIELD': '',
            'INCLUDE_BOUNDS': False,
            'INPUT': parameters['walkabilitylayerstreetnetwork'],
            'SPEED_FIELD': '',
            'START_POINTS': parameters['indivualsgeolocation'],
            'STRATEGY': 0,  # Shortest
            'TOLERANCE': 0,
            'TRAVEL_COST2': 800,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT_LINES': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ServiceAreaFromLayer_800'] = processing.run('native:serviceareafromlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # B400
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 400,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['indivualsgeolocation'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['B400'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # NDVI_B100 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['B100']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b100JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Service area (from layer)_400
        alg_params = {
            'DEFAULT_DIRECTION': 2,  # Both directions
            'DEFAULT_SPEED': 50,
            'DIRECTION_FIELD': '',
            'INCLUDE_BOUNDS': False,
            'INPUT': parameters['walkabilitylayerstreetnetwork'],
            'SPEED_FIELD': '',
            'START_POINTS': parameters['indivualsgeolocation'],
            'STRATEGY': 0,  # Shortest
            'TOLERANCE': 0,
            'TRAVEL_COST2': 400,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT_LINES': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ServiceAreaFromLayer_400'] = processing.run('native:serviceareafromlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # SPGS_wo_Buildings
        alg_params = {
            'INPUT': parameters['pgs (2)'],
            'OVERLAY': parameters['pgs (2) (3)'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Spgs_wo_buildings'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # B1100
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 1100,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['indivualsgeolocation'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['B1100'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Service area (from layer)_1200
        alg_params = {
            'DEFAULT_DIRECTION': 2,  # Both directions
            'DEFAULT_SPEED': 50,
            'DIRECTION_FIELD': '',
            'INCLUDE_BOUNDS': False,
            'INPUT': parameters['walkabilitylayerstreetnetwork'],
            'SPEED_FIELD': '',
            'START_POINTS': parameters['indivualsgeolocation'],
            'STRATEGY': 0,  # Shortest
            'TOLERANCE': 0,
            'TRAVEL_COST2': 1200,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT_LINES': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ServiceAreaFromLayer_1200'] = processing.run('native:serviceareafromlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Buffer_25_1200
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 25,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['ServiceAreaFromLayer_1200']['OUTPUT_LINES'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer_25_1200'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Field calculator BSA1200
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': '$area',
            'INPUT': outputs['Buffer_25_1200']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorBsa1200'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Buffer_25_800
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 25,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['ServiceAreaFromLayer_800']['OUTPUT_LINES'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer_25_800'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # B500
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 500,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['indivualsgeolocation'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['B500'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # B1300
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 1300,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['indivualsgeolocation'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['B1300'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA800 Clip
        alg_params = {
            'INPUT': outputs['Buffer_25_800']['OUTPUT'],
            'OVERLAY': parameters['pgs'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa800Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # Field calculator BSA1100
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': '$area',
            'INPUT': outputs['Buffer_25_1100']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorBsa1100'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # SPGS_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'SPGS',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': '$area',
            'INPUT': outputs['Spgs_wo_buildings']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Spgs_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # Service area (from layer)_600
        alg_params = {
            'DEFAULT_DIRECTION': 2,  # Both directions
            'DEFAULT_SPEED': 50,
            'DIRECTION_FIELD': '',
            'INCLUDE_BOUNDS': False,
            'INPUT': parameters['walkabilitylayerstreetnetwork'],
            'SPEED_FIELD': '',
            'START_POINTS': parameters['indivualsgeolocation'],
            'STRATEGY': 0,  # Shortest
            'TOLERANCE': 0,
            'TRAVEL_COST2': 600,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT_LINES': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ServiceAreaFromLayer_600'] = processing.run('native:serviceareafromlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # Service area (from layer)_700
        alg_params = {
            'DEFAULT_DIRECTION': 2,  # Both directions
            'DEFAULT_SPEED': 50,
            'DIRECTION_FIELD': '',
            'INCLUDE_BOUNDS': False,
            'INPUT': parameters['walkabilitylayerstreetnetwork'],
            'SPEED_FIELD': '',
            'START_POINTS': parameters['indivualsgeolocation'],
            'STRATEGY': 0,  # Shortest
            'TOLERANCE': 0,
            'TRAVEL_COST2': 700,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT_LINES': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ServiceAreaFromLayer_700'] = processing.run('native:serviceareafromlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # Buffer_25_300
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 25,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['ServiceAreaFromLayer_300']['OUTPUT_LINES'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer_25_300'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # Buffer_25_900
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 25,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['ServiceAreaFromLayer_900']['OUTPUT_LINES'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer_25_900'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # Conditional branch
        alg_params = {
        }
        outputs['ConditionalBranch'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # NDVI_SA800 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_800']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa800JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}

        # B1400
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 1400,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['indivualsgeolocation'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['B1400'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(38)
        if feedback.isCanceled():
            return {}

        # Buffer_25_1000
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 25,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['ServiceAreaFromLayer_1000']['OUTPUT_LINES'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer_25_1000'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(39)
        if feedback.isCanceled():
            return {}

        # Buffer_25_700
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 25,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['ServiceAreaFromLayer_700']['OUTPUT_LINES'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer_25_700'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(40)
        if feedback.isCanceled():
            return {}

        # Field calculator BSA300
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': '$area',
            'INPUT': outputs['Buffer_25_300']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorBsa300'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(41)
        if feedback.isCanceled():
            return {}

        # Service area (from layer)_200
        alg_params = {
            'DEFAULT_DIRECTION': 2,  # Both directions
            'DEFAULT_SPEED': 50,
            'DIRECTION_FIELD': '',
            'INCLUDE_BOUNDS': False,
            'INPUT': parameters['walkabilitylayerstreetnetwork'],
            'SPEED_FIELD': '',
            'START_POINTS': parameters['indivualsgeolocation'],
            'STRATEGY': 0,  # Shortest
            'TOLERANCE': 0,
            'TRAVEL_COST2': 200,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT_LINES': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ServiceAreaFromLayer_200'] = processing.run('native:serviceareafromlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(42)
        if feedback.isCanceled():
            return {}

        # NDVI_B1500 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['B1500']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1500JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(43)
        if feedback.isCanceled():
            return {}

        # NDVI_SA700 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_700']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa700JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(44)
        if feedback.isCanceled():
            return {}

        # B1200
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 1200,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['indivualsgeolocation'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['B1200'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(45)
        if feedback.isCanceled():
            return {}

        # B900
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 900,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['indivualsgeolocation'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['B900'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(46)
        if feedback.isCanceled():
            return {}

        # NDVI_SA300 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_300']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa300JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(47)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1100 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_1100']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1100JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(48)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA700 Clip
        alg_params = {
            'INPUT': outputs['Buffer_25_700']['OUTPUT'],
            'OVERLAY': parameters['pgs'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa700Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(49)
        if feedback.isCanceled():
            return {}

        # Service area (from layer)_1300
        alg_params = {
            'DEFAULT_DIRECTION': 2,  # Both directions
            'DEFAULT_SPEED': 50,
            'DIRECTION_FIELD': '',
            'INCLUDE_BOUNDS': False,
            'INPUT': parameters['walkabilitylayerstreetnetwork'],
            'SPEED_FIELD': '',
            'START_POINTS': parameters['indivualsgeolocation'],
            'STRATEGY': 0,  # Shortest
            'TOLERANCE': 0,
            'TRAVEL_COST2': 1300,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT_LINES': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ServiceAreaFromLayer_1300'] = processing.run('native:serviceareafromlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(50)
        if feedback.isCanceled():
            return {}

        # GS_play_BSA700_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_play_BSA700',
            'POINTS': parameters['pgs (2) (4)'],
            'POLYGONS': outputs['Buffer_25_700']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_play_bsa700_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(51)
        if feedback.isCanceled():
            return {}

        # B800
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 800,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['indivualsgeolocation'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['B800'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(52)
        if feedback.isCanceled():
            return {}

        # Service area (from layer)_100
        alg_params = {
            'DEFAULT_DIRECTION': 2,  # Both directions
            'DEFAULT_SPEED': 50,
            'DIRECTION_FIELD': '',
            'INCLUDE_BOUNDS': False,
            'INPUT': parameters['walkabilitylayerstreetnetwork'],
            'SPEED_FIELD': '',
            'START_POINTS': parameters['indivualsgeolocation'],
            'STRATEGY': 0,  # Shortest
            'TOLERANCE': 0,
            'TRAVEL_COST2': 100,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT_LINES': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ServiceAreaFromLayer_100'] = processing.run('native:serviceareafromlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(53)
        if feedback.isCanceled():
            return {}

        # PGS Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': parameters['pgs'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PgsFieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(54)
        if feedback.isCanceled():
            return {}

        # Buffer_25_1400
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 25,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['ServiceAreaFromLayer_1400']['OUTPUT_LINES'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer_25_1400'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(55)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1100 Clip
        alg_params = {
            'INPUT': outputs['Buffer_25_1100']['OUTPUT'],
            'OVERLAY': parameters['pgs'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1100Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(56)
        if feedback.isCanceled():
            return {}

        # Service area (from layer)_1500
        alg_params = {
            'DEFAULT_DIRECTION': 2,  # Both directions
            'DEFAULT_SPEED': 50,
            'DIRECTION_FIELD': '',
            'INCLUDE_BOUNDS': False,
            'INPUT': parameters['walkabilitylayerstreetnetwork'],
            'SPEED_FIELD': '',
            'START_POINTS': parameters['indivualsgeolocation'],
            'STRATEGY': 0,  # Shortest
            'TOLERANCE': 0,
            'TRAVEL_COST2': 1500,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT_LINES': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ServiceAreaFromLayer_1500'] = processing.run('native:serviceareafromlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(57)
        if feedback.isCanceled():
            return {}

        # NDVI_B300 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_b300JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_B300',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b300RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(58)
        if feedback.isCanceled():
            return {}

        # GS_play_BSA1000_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_play_BSA1000',
            'POINTS': parameters['pgs (2) (4)'],
            'POLYGONS': outputs['Buffer_25_1000']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_play_bsa1000_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(59)
        if feedback.isCanceled():
            return {}

        # NDVI_B400 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['B400']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b400JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(60)
        if feedback.isCanceled():
            return {}

        # Buffer_25_600
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 25,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['ServiceAreaFromLayer_600']['OUTPUT_LINES'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer_25_600'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(61)
        if feedback.isCanceled():
            return {}

        # B200
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 200,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['indivualsgeolocation'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['B200'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(62)
        if feedback.isCanceled():
            return {}

        # PRGS_wo_buildings
        alg_params = {
            'INPUT': parameters['pgs (2) (2)'],
            'OVERLAY': parameters['pgs (2) (3)'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Prgs_wo_buildings'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(63)
        if feedback.isCanceled():
            return {}

        # GS_play_BSA1100_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_play_BSA1100',
            'POINTS': parameters['pgs (2) (4)'],
            'POLYGONS': outputs['Buffer_25_1100']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_play_bsa1100_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(64)
        if feedback.isCanceled():
            return {}

        # NDVI_B700 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['B700']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b700JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(65)
        if feedback.isCanceled():
            return {}

        # Field calculator BSA800
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': '$area',
            'INPUT': outputs['Buffer_25_800']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorBsa800'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(66)
        if feedback.isCanceled():
            return {}

        # NDVI_B800 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['B800']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b800JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(67)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1400 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_1400']['OUTPUT'],
            'JOIN': outputs['PgsFieldCalculator']['OUTPUT'],
            'JOIN_FIELDS': ['PGS_area'],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1400JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(68)
        if feedback.isCanceled():
            return {}

        # Service area (from layer)_500
        alg_params = {
            'DEFAULT_DIRECTION': 2,  # Both directions
            'DEFAULT_SPEED': 50,
            'DIRECTION_FIELD': '',
            'INCLUDE_BOUNDS': False,
            'INPUT': parameters['walkabilitylayerstreetnetwork'],
            'SPEED_FIELD': '',
            'START_POINTS': parameters['indivualsgeolocation'],
            'STRATEGY': 0,  # Shortest
            'TOLERANCE': 0,
            'TRAVEL_COST2': 500,
            'VALUE_BACKWARD': '',
            'VALUE_BOTH': '',
            'VALUE_FORWARD': '',
            'OUTPUT_LINES': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ServiceAreaFromLayer_500'] = processing.run('native:serviceareafromlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(69)
        if feedback.isCanceled():
            return {}

        # NDVI_B800 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_b800JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_B800',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b800RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(70)
        if feedback.isCanceled():
            return {}

        # PRGS_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PRGS',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': '$area',
            'INPUT': outputs['Prgs_wo_buildings']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Prgs_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(71)
        if feedback.isCanceled():
            return {}

        # GS_play_BSA800_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_play_BSA800',
            'POINTS': parameters['pgs (2) (4)'],
            'POLYGONS': outputs['Buffer_25_800']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_play_bsa800_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(72)
        if feedback.isCanceled():
            return {}

        # NDVI_B1500 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_b1500JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_B1500',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1500RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(73)
        if feedback.isCanceled():
            return {}

        # PRGS_Join attributes by nearest
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELDS_TO_COPY': ['PRGS'],
            'INPUT': parameters['indivualsgeolocation'],
            'INPUT_2': outputs['Prgs_fieldCalculator']['OUTPUT'],
            'MAX_DISTANCE': 10,
            'NEIGHBORS': 1,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Prgs_joinAttributesByNearest'] = processing.run('native:joinbynearest', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(74)
        if feedback.isCanceled():
            return {}

        # NDVI_B100 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_b100JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_B100',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b100RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(75)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1400 Rename field
        alg_params = {
            'FIELD': 'PGS_area_sum',
            'INPUT': outputs['Pgs_a2_sa1400JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'PGS_A2_SA1400',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1400RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(76)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1100 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_1100']['OUTPUT'],
            'JOIN': outputs['PgsFieldCalculator']['OUTPUT'],
            'JOIN_FIELDS': ['PGS_area'],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1100JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(77)
        if feedback.isCanceled():
            return {}

        # Buffer_25_100
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 25,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['ServiceAreaFromLayer_100']['OUTPUT_LINES'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer_25_100'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(78)
        if feedback.isCanceled():
            return {}

        # SPGS_Join attributes by nearest
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELDS_TO_COPY': ['SPGS'],
            'INPUT': parameters['indivualsgeolocation'],
            'INPUT_2': outputs['Spgs_fieldCalculator']['OUTPUT'],
            'MAX_DISTANCE': 10,
            'NEIGHBORS': 1,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Spgs_joinAttributesByNearest'] = processing.run('native:joinbynearest', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(79)
        if feedback.isCanceled():
            return {}

        # B600
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 600,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['indivualsgeolocation'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['B600'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(80)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA900 Clip
        alg_params = {
            'INPUT': outputs['Buffer_25_900']['OUTPUT'],
            'OVERLAY': parameters['pgs'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa900Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(81)
        if feedback.isCanceled():
            return {}

        # B1000
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 1000,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['indivualsgeolocation'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['B1000'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(82)
        if feedback.isCanceled():
            return {}

        # Field calculator BSA900
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': '$area',
            'INPUT': outputs['Buffer_25_900']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorBsa900'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(83)
        if feedback.isCanceled():
            return {}

        # GS_sports_BSA1000_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_sports_BSA1000',
            'POINTS': parameters['pgs (2) (4) (2)'],
            'POLYGONS': outputs['Gs_play_bsa1000_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_sports_bsa1000_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(84)
        if feedback.isCanceled():
            return {}

        # GS_play_BSA900_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_play_BSA900',
            'POINTS': parameters['pgs (2) (4)'],
            'POLYGONS': outputs['Buffer_25_900']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_play_bsa900_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(85)
        if feedback.isCanceled():
            return {}

        # GS_play_BSA1200_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_play_BSA1200',
            'POINTS': parameters['pgs (2) (4)'],
            'POLYGONS': outputs['Buffer_25_1200']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_play_bsa1200_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(86)
        if feedback.isCanceled():
            return {}

        # Buffer_25_1300
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 25,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['ServiceAreaFromLayer_1300']['OUTPUT_LINES'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer_25_1300'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(87)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1000 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_1000']['OUTPUT'],
            'JOIN': outputs['PgsFieldCalculator']['OUTPUT'],
            'JOIN_FIELDS': ['PGS_area'],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1000JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(88)
        if feedback.isCanceled():
            return {}

        # Field calculator BSA600
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': '$area',
            'INPUT': outputs['Buffer_25_600']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorBsa600'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(89)
        if feedback.isCanceled():
            return {}

        # GS_play_BSA100_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_play_BSA100',
            'POINTS': parameters['pgs (2) (4)'],
            'POLYGONS': outputs['Buffer_25_100']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_play_bsa100_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(90)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1200 Clip
        alg_params = {
            'INPUT': outputs['Buffer_25_1200']['OUTPUT'],
            'OVERLAY': parameters['pgs'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1200Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(91)
        if feedback.isCanceled():
            return {}

        # GS_sports_BSA1200_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_sports_BSA1200',
            'POINTS': parameters['pgs (2) (4) (2)'],
            'POLYGONS': outputs['Gs_play_bsa1200_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_sports_bsa1200_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(92)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1100 Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_in_SA1100',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': outputs['Pgs_in_sa1100Clip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1100FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(93)
        if feedback.isCanceled():
            return {}

        # GS_play_BSA1400_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_play_BSA1400',
            'POINTS': parameters['pgs (2) (4)'],
            'POLYGONS': outputs['Buffer_25_1400']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_play_bsa1400_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(94)
        if feedback.isCanceled():
            return {}

        # GS_walk_BSA1200_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_walk_BSA1200',
            'POINTS': parameters['pgs (2) (4) (2) (2)'],
            'POLYGONS': outputs['Gs_sports_bsa1200_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_walk_bsa1200_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(95)
        if feedback.isCanceled():
            return {}

        # NDVI_B900 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['B900']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b900JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(96)
        if feedback.isCanceled():
            return {}

        # Field calculator BSA700
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': outputs['Buffer_25_700']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorBsa700'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(97)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA600 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_600']['OUTPUT'],
            'JOIN': outputs['PgsFieldCalculator']['OUTPUT'],
            'JOIN_FIELDS': ['PGS_area'],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa600JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(98)
        if feedback.isCanceled():
            return {}

        # Buffer_25_200
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 25,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['ServiceAreaFromLayer_200']['OUTPUT_LINES'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer_25_200'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(99)
        if feedback.isCanceled():
            return {}

        # NDVI_B1100 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['B1100']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1100JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(100)
        if feedback.isCanceled():
            return {}

        # GS_sports_BSA800_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_sports_BSA800',
            'POINTS': parameters['pgs (2) (4) (2)'],
            'POLYGONS': outputs['Gs_play_bsa800_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_sports_bsa800_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(101)
        if feedback.isCanceled():
            return {}

        # NDVI_SA300 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_sa300JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_SA300',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa300RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(102)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA100 Clip
        alg_params = {
            'INPUT': outputs['Buffer_25_100']['OUTPUT'],
            'OVERLAY': parameters['pgs'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa100Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(103)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1000 Clip
        alg_params = {
            'INPUT': outputs['Buffer_25_1000']['OUTPUT'],
            'OVERLAY': parameters['pgs'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1000Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(104)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1200 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_1200']['OUTPUT'],
            'JOIN': outputs['PgsFieldCalculator']['OUTPUT'],
            'JOIN_FIELDS': ['PGS_area'],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1200JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(105)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1400 Clip
        alg_params = {
            'INPUT': outputs['Buffer_25_1400']['OUTPUT'],
            'OVERLAY': parameters['pgs'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1400Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(106)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1000 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_1000']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1000JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(107)
        if feedback.isCanceled():
            return {}

        # GS_sports_BSA700_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_sports_BSA700',
            'POINTS': parameters['pgs (2) (4) (2)'],
            'POLYGONS': outputs['Gs_play_bsa700_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_sports_bsa700_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(108)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA300 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_300']['OUTPUT'],
            'JOIN': outputs['PgsFieldCalculator']['OUTPUT'],
            'JOIN_FIELDS': ['PGS_area'],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa300JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(109)
        if feedback.isCanceled():
            return {}

        # NDVI_B1300 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['B1300']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1300JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(110)
        if feedback.isCanceled():
            return {}

        # NDVI_SA100 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_100']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa100JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(111)
        if feedback.isCanceled():
            return {}

        # GS_play_BSA600_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_play_BSA600',
            'POINTS': parameters['pgs (2) (4)'],
            'POLYGONS': outputs['Buffer_25_600']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_play_bsa600_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(112)
        if feedback.isCanceled():
            return {}

        # Field calculator BSA1000
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': '$area',
            'INPUT': outputs['Buffer_25_1000']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorBsa1000'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(113)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA300 Clip
        alg_params = {
            'INPUT': outputs['Buffer_25_300']['OUTPUT'],
            'OVERLAY': parameters['pgs'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa300Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(114)
        if feedback.isCanceled():
            return {}

        # Buffer_25_1500
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 25,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['ServiceAreaFromLayer_1500']['OUTPUT_LINES'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer_25_1500'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(115)
        if feedback.isCanceled():
            return {}

        # Field calculator BSA1400
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': '$area',
            'INPUT': outputs['Buffer_25_1400']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorBsa1400'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(116)
        if feedback.isCanceled():
            return {}

        # GS_play_BSA1300_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_play_BSA1300',
            'POINTS': parameters['pgs (2) (4)'],
            'POLYGONS': outputs['Buffer_25_1300']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_play_bsa1300_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(117)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1100 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_sa1100JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_SA1100',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1100RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(118)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA800 Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_in_SA800',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': outputs['Pgs_in_sa800Clip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa800FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(119)
        if feedback.isCanceled():
            return {}

        # NDVI_B700 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_b700JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_B700',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b700RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(120)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1200 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_1200']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1200JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(121)
        if feedback.isCanceled():
            return {}

        # NDVI_B600 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['B600']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b600JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(122)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA800 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_800']['OUTPUT'],
            'JOIN': outputs['PgsFieldCalculator']['OUTPUT'],
            'JOIN_FIELDS': ['PGS_area'],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa800JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(123)
        if feedback.isCanceled():
            return {}

        # Buffer_25_400
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 25,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['ServiceAreaFromLayer_400']['OUTPUT_LINES'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer_25_400'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(124)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1300 Clip
        alg_params = {
            'INPUT': outputs['Buffer_25_1300']['OUTPUT'],
            'OVERLAY': parameters['pgs'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1300Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(125)
        if feedback.isCanceled():
            return {}

        # GS_play_BSA300_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_play_BSA300',
            'POINTS': parameters['pgs (2) (4)'],
            'POLYGONS': outputs['Buffer_25_300']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_play_bsa300_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(126)
        if feedback.isCanceled():
            return {}

        # GS_sports_BSA1300_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_sports_BSA1300',
            'POINTS': parameters['pgs (2) (4) (2)'],
            'POLYGONS': outputs['Gs_play_bsa1300_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_sports_bsa1300_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(127)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA900 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_900']['OUTPUT'],
            'JOIN': outputs['PgsFieldCalculator']['OUTPUT'],
            'JOIN_FIELDS': ['PGS_area'],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa900JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(128)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1400 Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_in_SA1400',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': outputs['Pgs_in_sa1400Clip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1400FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(129)
        if feedback.isCanceled():
            return {}

        # NDVI_B1300 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_b1300JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_B1300',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1300RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(130)
        if feedback.isCanceled():
            return {}

        # GS_sports_BSA1100_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_sports_BSA1100',
            'POINTS': parameters['pgs (2) (4) (2)'],
            'POLYGONS': outputs['Gs_play_bsa1100_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_sports_bsa1100_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(131)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA700 Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_in_SA700',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': outputs['Pgs_in_sa700Clip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa700FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(132)
        if feedback.isCanceled():
            return {}

        # NDVI_SA800 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_sa800JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_SA800',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa800RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(133)
        if feedback.isCanceled():
            return {}

        # GS_play_BSA200_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_play_BSA200',
            'POINTS': parameters['pgs (2) (4)'],
            'POLYGONS': outputs['Buffer_25_200']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_play_bsa200_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(134)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value BSA1100_area
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA1100'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['FieldCalculatorBsa1100']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa1100FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueBsa1100_area'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(135)
        if feedback.isCanceled():
            return {}

        # Field calculator BSA100
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': '$area',
            'INPUT': outputs['Buffer_25_100']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorBsa100'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(136)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1500 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_1500']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1500JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(137)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA800 Rename field
        alg_params = {
            'FIELD': 'PGS_area_sum',
            'INPUT': outputs['Pgs_a2_sa800JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'PGS_A2_SA800',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa800RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(138)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA100 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_100']['OUTPUT'],
            'JOIN': outputs['PgsFieldCalculator']['OUTPUT'],
            'JOIN_FIELDS': ['PGS_area'],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa100JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(139)
        if feedback.isCanceled():
            return {}

        # NDVI_B500 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['B500']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b500JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(140)
        if feedback.isCanceled():
            return {}

        # NDVI_B1100 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_b1100JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_B1100',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1100RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(141)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1300 Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_in_SA1300',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': outputs['Pgs_in_sa1300Clip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1300FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(142)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA700 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_700']['OUTPUT'],
            'JOIN': outputs['PgsFieldCalculator']['OUTPUT'],
            'JOIN_FIELDS': ['PGS_area'],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa700JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(143)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1400 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_1400']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1400JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(144)
        if feedback.isCanceled():
            return {}

        # GS_walk_BSA1000_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_walk_BSA1000',
            'POINTS': parameters['pgs (2) (4) (2) (2)'],
            'POLYGONS': outputs['Gs_sports_bsa1000_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_walk_bsa1000_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(145)
        if feedback.isCanceled():
            return {}

        # NDVI_SA700 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_sa700JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_SA700',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa700RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(146)
        if feedback.isCanceled():
            return {}

        # Buffer_25_500
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 25,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['ServiceAreaFromLayer_500']['OUTPUT_LINES'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer_25_500'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(147)
        if feedback.isCanceled():
            return {}

        # GS_sports_BSA600_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_sports_BSA600',
            'POINTS': parameters['pgs (2) (4) (2)'],
            'POLYGONS': outputs['Gs_play_bsa600_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_sports_bsa600_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(148)
        if feedback.isCanceled():
            return {}

        # GS_gard_BSA1200_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_gard_BSA1200',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_walk_bsa1200_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_gard_bsa1200_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(149)
        if feedback.isCanceled():
            return {}

        # NDVI_SA900 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_900']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa900JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(150)
        if feedback.isCanceled():
            return {}

        # GS_walk_BSA800_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_walk_BSA800',
            'POINTS': parameters['pgs (2) (4) (2) (2)'],
            'POLYGONS': outputs['Gs_sports_bsa800_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_walk_bsa800_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(151)
        if feedback.isCanceled():
            return {}

        # GS_gard_BSA1000_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_gard_BSA1000',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_walk_bsa1000_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_gard_bsa1000_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(152)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA900 Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_in_SA900',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': outputs['Pgs_in_sa900Clip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa900FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(153)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA200 Clip
        alg_params = {
            'INPUT': outputs['Buffer_25_200']['OUTPUT'],
            'OVERLAY': parameters['pgs'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa200Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(154)
        if feedback.isCanceled():
            return {}

        # NDVI_B1400 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['B1400']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1400JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(155)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1200 Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_in_SA1200',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': outputs['Pgs_in_sa1200Clip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1200FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(156)
        if feedback.isCanceled():
            return {}

        # NDVI_SA200 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_200']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa200JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(157)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1200 Rename field
        alg_params = {
            'FIELD': 'PGS_area_sum',
            'INPUT': outputs['Pgs_a2_sa1200JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'PGS_A2_SA1200',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1200RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(158)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1200 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_sa1200JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_SA1200',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1200RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(159)
        if feedback.isCanceled():
            return {}

        # PRGS Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PRGS'],
            'FIELD_2': parameters['idfield'],
            'INPUT': parameters['indivualsgeolocation'],
            'INPUT_2': outputs['Prgs_joinAttributesByNearest']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PrgsJoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(160)
        if feedback.isCanceled():
            return {}

        # GS_play_BSA500_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_play_BSA500',
            'POINTS': parameters['pgs (2) (4)'],
            'POLYGONS': outputs['Buffer_25_500']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_play_bsa500_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(161)
        if feedback.isCanceled():
            return {}

        # NDVI_B1200 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['B1200']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1200JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(162)
        if feedback.isCanceled():
            return {}

        # NDVI_B400 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_b400JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_B400',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b400RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(163)
        if feedback.isCanceled():
            return {}

        # NDVI_SA400 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_400']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa400JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(164)
        if feedback.isCanceled():
            return {}

        # NDVI_B900 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_b900JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_B900',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b900RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(165)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1300 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_1300']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1300JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(166)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1100 Rename field
        alg_params = {
            'FIELD': 'PGS_area_sum',
            'INPUT': outputs['Pgs_a2_sa1100JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'PGS_A2_SA1100',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1100RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(167)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA300 Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_in_SA300',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': outputs['Pgs_in_sa300Clip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa300FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(168)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA200 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_200']['OUTPUT'],
            'JOIN': outputs['PgsFieldCalculator']['OUTPUT'],
            'JOIN_FIELDS': ['PGS_area'],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa200JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(169)
        if feedback.isCanceled():
            return {}

        # GS_walk_BSA1100_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_walk_BSA1100',
            'POINTS': parameters['pgs (2) (4) (2) (2)'],
            'POLYGONS': outputs['Gs_sports_bsa1100_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_walk_bsa1100_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(170)
        if feedback.isCanceled():
            return {}

        # GS_sports_BSA100_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_sports_BSA100',
            'POINTS': parameters['pgs (2) (4) (2)'],
            'POLYGONS': outputs['Gs_play_bsa100_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_sports_bsa100_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(171)
        if feedback.isCanceled():
            return {}

        # NDVI_B1000 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['B1000']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1000JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(172)
        if feedback.isCanceled():
            return {}

        # GS_sports_BSA500_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_sports_BSA500',
            'POINTS': parameters['pgs (2) (4) (2)'],
            'POLYGONS': outputs['Gs_play_bsa500_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_sports_bsa500_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(173)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value BSA1400_area
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA1400'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['FieldCalculatorBsa1400']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa1400FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueBsa1400_area'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(174)
        if feedback.isCanceled():
            return {}

        # GS_gard_BSA800_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_gard_BSA800',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_walk_bsa800_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_gard_bsa800_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(175)
        if feedback.isCanceled():
            return {}

        # NDVI_B1200 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_b1200JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_B1200',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1200RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(176)
        if feedback.isCanceled():
            return {}

        # GS_social_BSA800_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_social_BSA800',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_gard_bsa800_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_social_bsa800_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(177)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA600 Rename field
        alg_params = {
            'FIELD': 'PGS_area_sum',
            'INPUT': outputs['Pgs_a2_sa600JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'PGS_A2_SA600',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa600RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(178)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value BSA700_area
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA700'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['FieldCalculatorBsa700']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa700FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueBsa700_area'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(179)
        if feedback.isCanceled():
            return {}

        # NDVI_B200 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['B200']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b200JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(180)
        if feedback.isCanceled():
            return {}

        # NDVI_B1400 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_b1400JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_B1400',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1400RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(181)
        if feedback.isCanceled():
            return {}

        # NDVI_SA600 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_600']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa600JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(182)
        if feedback.isCanceled():
            return {}

        # GS_sports_BSA200_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_sports_BSA200',
            'POINTS': parameters['pgs (2) (4) (2)'],
            'POLYGONS': outputs['Gs_play_bsa200_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_sports_bsa200_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(183)
        if feedback.isCanceled():
            return {}

        # GS_play_BSA1500_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_play_BSA1500',
            'POINTS': parameters['pgs (2) (4)'],
            'POLYGONS': outputs['Buffer_25_1500']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_play_bsa1500_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(184)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1000 Rename field
        alg_params = {
            'FIELD': 'PGS_area_sum',
            'INPUT': outputs['Pgs_a2_sa1000JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'PGS_A2_SA1000',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1000RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(185)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA600 Clip
        alg_params = {
            'INPUT': outputs['Buffer_25_600']['OUTPUT'],
            'OVERLAY': parameters['pgs'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa600Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(186)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value BSA1200_area
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA1200'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['FieldCalculatorBsa1200']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa1200FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueBsa1200_area'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(187)
        if feedback.isCanceled():
            return {}

        # NDVI_SA100 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_sa100JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_SA100',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa100RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(188)
        if feedback.isCanceled():
            return {}

        # Field calculator PGS_ratio_1400
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_ratio_1400',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'CASE\n\tWHEN "PGS_in_SA1400" = NULL THEN 0\n\tELSE "PGS_in_SA1400"/"area"\nEND\t',
            'INPUT': outputs['JoinAttributesByFieldValueBsa1400_area']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPgs_ratio_1400'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(189)
        if feedback.isCanceled():
            return {}

        # GS_sports_BSA900_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_sports_BSA900',
            'POINTS': parameters['pgs (2) (4) (2)'],
            'POLYGONS': outputs['Gs_play_bsa900_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_sports_bsa900_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(190)
        if feedback.isCanceled():
            return {}

        # NDVI_SA500 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_500']['OUTPUT'],
            'JOIN': parameters['ndvi'],
            'JOIN_FIELDS': [''],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [6],  # mean
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa500JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(191)
        if feedback.isCanceled():
            return {}

        # Field calculator BSA400
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': '$area',
            'INPUT': outputs['Buffer_25_400']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorBsa400'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(192)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA100 Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_in_SA100',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': outputs['Pgs_in_sa100Clip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa100FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(193)
        if feedback.isCanceled():
            return {}

        # NDVI_B500 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_b500JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_B500',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b500RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(194)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value BSA800_area
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA800'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['FieldCalculatorBsa800']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa800FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueBsa800_area'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(195)
        if feedback.isCanceled():
            return {}

        # Field calculator BSA1300
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': '$area',
            'INPUT': outputs['Buffer_25_1300']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorBsa1300'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(196)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value BSA100_area
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA100'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['FieldCalculatorBsa100']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa100FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueBsa100_area'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(197)
        if feedback.isCanceled():
            return {}

        # NDVI_B100 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_B100'],
            'FIELD_2': parameters['idfield'],
            'INPUT': parameters['indivualsgeolocation'],
            'INPUT_2': outputs['Ndvi_b100RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b100JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(198)
        if feedback.isCanceled():
            return {}

        # NDVI_SA900 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_sa900JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_SA900',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa900RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(199)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1000 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_sa1000JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_SA1000',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1000RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(200)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1000 Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_in_SA1000',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': outputs['Pgs_in_sa1000Clip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1000FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(201)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1300 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_1300']['OUTPUT'],
            'JOIN': outputs['PgsFieldCalculator']['OUTPUT'],
            'JOIN_FIELDS': ['PGS_area'],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1300JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(202)
        if feedback.isCanceled():
            return {}

        # GS_sports_BSA1400_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_sports_BSA1400',
            'POINTS': parameters['pgs (2) (4) (2)'],
            'POLYGONS': outputs['Gs_play_bsa1400_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_sports_bsa1400_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(203)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA900 Rename field
        alg_params = {
            'FIELD': 'PGS_area_sum',
            'INPUT': outputs['Pgs_a2_sa900JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'PGS_A2_SA900',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa900RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(204)
        if feedback.isCanceled():
            return {}

        # GS_walk_BSA600_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_walk_BSA600',
            'POINTS': parameters['pgs (2) (4) (2) (2)'],
            'POLYGONS': outputs['Gs_sports_bsa600_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_walk_bsa600_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(205)
        if feedback.isCanceled():
            return {}

        # NDVI_SA600 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_sa600JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_SA600',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa600RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(206)
        if feedback.isCanceled():
            return {}

        # GS_walk_BSA1300_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_walk_BSA1300',
            'POINTS': parameters['pgs (2) (4) (2) (2)'],
            'POLYGONS': outputs['Gs_sports_bsa1300_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_walk_bsa1300_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(207)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA700 Rename field
        alg_params = {
            'FIELD': 'PGS_area_sum',
            'INPUT': outputs['Pgs_a2_sa700JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'PGS_A2_SA700',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa700RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(208)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA400 Clip
        alg_params = {
            'INPUT': outputs['Buffer_25_400']['OUTPUT'],
            'OVERLAY': parameters['pgs'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa400Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(209)
        if feedback.isCanceled():
            return {}

        # GS_social_BSA1000_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_social_BSA1000',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_gard_bsa1000_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_social_bsa1000_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(210)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value BSA1000_area
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA1000'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['FieldCalculatorBsa1000']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa1000FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueBsa1000_area'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(211)
        if feedback.isCanceled():
            return {}

        # GS_gard_BSA600_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_gard_BSA600',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_walk_bsa600_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_gard_bsa600_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(212)
        if feedback.isCanceled():
            return {}

        # Field calculator BSA1500
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': '$area',
            'INPUT': outputs['Buffer_25_1500']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorBsa1500'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(213)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1400 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_sa1400JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_SA1400',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1400RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(214)
        if feedback.isCanceled():
            return {}

        # GS_social_BSA1200_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_social_BSA1200',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_gard_bsa1200_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_social_bsa1200_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(215)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1300 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_sa1300JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_SA1300',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1300RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(216)
        if feedback.isCanceled():
            return {}

        # GS_walk_BSA700_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_walk_BSA700',
            'POINTS': parameters['pgs (2) (4) (2) (2)'],
            'POLYGONS': outputs['Gs_sports_bsa700_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_walk_bsa700_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(217)
        if feedback.isCanceled():
            return {}

        # GS_walk_BSA500_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_walk_BSA500',
            'POINTS': parameters['pgs (2) (4) (2) (2)'],
            'POLYGONS': outputs['Gs_sports_bsa500_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_walk_bsa500_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(218)
        if feedback.isCanceled():
            return {}

        # NDVI_B200 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_b200JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_B200',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b200RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(219)
        if feedback.isCanceled():
            return {}

        # GS_play_BSA400_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_play_BSA400',
            'POINTS': parameters['pgs (2) (4)'],
            'POLYGONS': outputs['Buffer_25_400']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_play_bsa400_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(220)
        if feedback.isCanceled():
            return {}

        # Field calculator BSA200
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': '$area',
            'INPUT': outputs['Buffer_25_200']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorBsa200'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(221)
        if feedback.isCanceled():
            return {}

        # GS_sports_BSA300_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_sports_BSA300',
            'POINTS': parameters['pgs (2) (4) (2)'],
            'POLYGONS': outputs['Gs_play_bsa300_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_sports_bsa300_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(222)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA500 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_500']['OUTPUT'],
            'JOIN': outputs['PgsFieldCalculator']['OUTPUT'],
            'JOIN_FIELDS': ['PGS_area'],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa500JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(223)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value BSA1300_area
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA1300'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['FieldCalculatorBsa1300']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa1300FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueBsa1300_area'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(224)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA300 Rename field
        alg_params = {
            'FIELD': 'PGS_area_sum',
            'INPUT': outputs['Pgs_a2_sa300JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'PGS_A2_SA300',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa300RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(225)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA200 Rename field
        alg_params = {
            'FIELD': 'PGS_area_sum',
            'INPUT': outputs['Pgs_a2_sa200JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'PGS_A2_SA200',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa200RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(226)
        if feedback.isCanceled():
            return {}

        # GS_gard_BSA1100_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_gard_BSA1100',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_walk_bsa1100_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_gard_bsa1100_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(227)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA100 Rename field
        alg_params = {
            'FIELD': 'PGS_area_sum',
            'INPUT': outputs['Pgs_a2_sa100JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'PGS_A2_SA100',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa100RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(228)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA500 Rename field
        alg_params = {
            'FIELD': 'PGS_area_sum',
            'INPUT': outputs['Pgs_a2_sa500JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'PGS_A2_SA500',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa500RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(229)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA400 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_400']['OUTPUT'],
            'JOIN': outputs['PgsFieldCalculator']['OUTPUT'],
            'JOIN_FIELDS': ['PGS_area'],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa400JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(230)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA500 Clip
        alg_params = {
            'INPUT': outputs['Buffer_25_500']['OUTPUT'],
            'OVERLAY': parameters['pgs'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa500Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(231)
        if feedback.isCanceled():
            return {}

        # GS_sports_BSA1500_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_sports_BSA1500',
            'POINTS': parameters['pgs (2) (4) (2)'],
            'POLYGONS': outputs['Gs_play_bsa1500_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_sports_bsa1500_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(232)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA500 Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_in_SA500',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': outputs['Pgs_in_sa500Clip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa500FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(233)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1500 Clip
        alg_params = {
            'INPUT': outputs['Buffer_25_1500']['OUTPUT'],
            'OVERLAY': parameters['pgs'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1500Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(234)
        if feedback.isCanceled():
            return {}

        # GS_walk_BSA200_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_walk_BSA200',
            'POINTS': parameters['pgs (2) (4) (2) (2)'],
            'POLYGONS': outputs['Gs_sports_bsa200_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_walk_bsa200_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(235)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value BSA300_area
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA300'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['FieldCalculatorBsa300']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa300FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueBsa300_area'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(236)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1500 Join attributes by location (summary)
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['Buffer_25_1500']['OUTPUT'],
            'JOIN': outputs['PgsFieldCalculator']['OUTPUT'],
            'JOIN_FIELDS': ['PGS_area'],
            'PREDICATE': [0],  # intersects
            'SUMMARIES': [5],  # sum
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1500JoinAttributesByLocationSummary'] = processing.run('qgis:joinbylocationsummary', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(237)
        if feedback.isCanceled():
            return {}

        # GS_gard_BSA700_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_gard_BSA700',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_walk_bsa700_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_gard_bsa700_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(238)
        if feedback.isCanceled():
            return {}

        # Field calculator BSA500
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': '$area',
            'INPUT': outputs['Buffer_25_500']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorBsa500'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(239)
        if feedback.isCanceled():
            return {}

        # NDVI_SA500 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_sa500JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_SA500',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa500RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(240)
        if feedback.isCanceled():
            return {}

        # NDVI_B600 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_b600JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_B600',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b600RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(241)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA200 Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_in_SA200',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': outputs['Pgs_in_sa200Clip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa200FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(242)
        if feedback.isCanceled():
            return {}

        # GS_gard_BSA1300_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_gard_BSA1300',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_walk_bsa1300_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_gard_bsa1300_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(243)
        if feedback.isCanceled():
            return {}

        # Field calculator PGS_ratio_1100
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_ratio_1100',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'CASE\n\tWHEN "PGS_in_SA1100" = NULL THEN 0\n\tELSE "PGS_in_SA1100"/"area"\nEND\t',
            'INPUT': outputs['JoinAttributesByFieldValueBsa1100_area']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPgs_ratio_1100'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(244)
        if feedback.isCanceled():
            return {}

        # GS_other_BSA1200_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_other_BSA1200',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_social_bsa1200_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_other_bsa1200_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(245)
        if feedback.isCanceled():
            return {}

        # GS_uses_sum_BSA1200_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_sum_BSA1200',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"GS_play_BSA1200" + "GS_sports_BSA1200" + "GS_walk_BSA1200" + "GS_gard_BSA1200" + "GS_social_BSA1200" + "GS_other_BSA1200"',
            'INPUT': outputs['Gs_other_bsa1200_countPointsInPolygon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_sum_bsa1200_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(246)
        if feedback.isCanceled():
            return {}

        # NDVI_B1000 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_b1000JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_B1000',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1000RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(247)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1500 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_sa1500JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_SA1500',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1500RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(248)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA400 Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_in_SA400',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': outputs['Pgs_in_sa400Clip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa400FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(249)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1300 Rename field
        alg_params = {
            'FIELD': 'PGS_area_sum',
            'INPUT': outputs['Pgs_a2_sa1300JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'PGS_A2_SA1300',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1300RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(250)
        if feedback.isCanceled():
            return {}

        # GS_social_BSA1300_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_social_BSA1300',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_gard_bsa1300_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_social_bsa1300_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(251)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value BSA900_area
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA900'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['FieldCalculatorBsa900']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa900FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueBsa900_area'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(252)
        if feedback.isCanceled():
            return {}

        # NDVI_SA200 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_sa200JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_SA200',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa200RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(253)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA600 Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_in_SA600',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': outputs['Pgs_in_sa600Clip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa600FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(254)
        if feedback.isCanceled():
            return {}

        # GS_walk_BSA1500_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_walk_BSA1500',
            'POINTS': parameters['pgs (2) (4) (2) (2)'],
            'POLYGONS': outputs['Gs_sports_bsa1500_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_walk_bsa1500_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(255)
        if feedback.isCanceled():
            return {}

        # Field calculator PGS_ratio_100
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_ratio_100',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'CASE\n\tWHEN "PGS_in_SA100" = NULL THEN 0\n\tELSE "PGS_in_SA100"/"area"\nEND\t',
            'INPUT': outputs['JoinAttributesByFieldValueBsa100_area']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPgs_ratio_100'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(256)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1500 Rename field
        alg_params = {
            'FIELD': 'PGS_area_sum',
            'INPUT': outputs['Pgs_a2_sa1500JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'PGS_A2_SA1500',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1500RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(257)
        if feedback.isCanceled():
            return {}

        # GS_walk_BSA100_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_walk_BSA100',
            'POINTS': parameters['pgs (2) (4) (2) (2)'],
            'POLYGONS': outputs['Gs_sports_bsa100_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_walk_bsa100_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(258)
        if feedback.isCanceled():
            return {}

        # GS_social_BSA700_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_social_BSA700',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_gard_bsa700_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_social_bsa700_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(259)
        if feedback.isCanceled():
            return {}

        # GS_other_BSA1300_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_other_BSA1300',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_social_bsa1300_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_other_bsa1300_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(260)
        if feedback.isCanceled():
            return {}

        # Field calculator PGS_ratio_800
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_ratio_800',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'CASE\n\tWHEN "PGS_in_SA800" = NULL THEN 0\n\tELSE "PGS_in_SA800"/"area"\nEND\t',
            'INPUT': outputs['JoinAttributesByFieldValueBsa800_area']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPgs_ratio_800'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(261)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA100 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_A2_SA100'],
            'FIELD_2': parameters['idfield'],
            'INPUT': parameters['indivualsgeolocation'],
            'INPUT_2': outputs['Pgs_a2_sa100RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa100JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(262)
        if feedback.isCanceled():
            return {}

        # SPGS Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['SPGS'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['PrgsJoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Spgs_joinAttributesByNearest']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['SemipublicPrivateGreenSpacesM2PerIndividual']
        }
        outputs['SpgsJoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SemipublicPrivateGreenSpacesM2PerIndividual'] = outputs['SpgsJoinAttributesByFieldValue']['OUTPUT']

        feedback.setCurrentStep(263)
        if feedback.isCanceled():
            return {}

        # GS_walk_BSA1400_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_walk_BSA1400',
            'POINTS': parameters['pgs (2) (4) (2) (2)'],
            'POLYGONS': outputs['Gs_sports_bsa1400_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_walk_bsa1400_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(264)
        if feedback.isCanceled():
            return {}

        # GS_gard_BSA200_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_gard_BSA200',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_walk_bsa200_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_gard_bsa200_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(265)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value BSA200_area
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA200'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['FieldCalculatorBsa200']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa200FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueBsa200_area'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(266)
        if feedback.isCanceled():
            return {}

        # Field calculator PGS_ratio_1300
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_ratio_1300',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'CASE\n\tWHEN "PGS_in_SA1300" = NULL THEN 0\n\tELSE "PGS_in_SA1300"/"area"\nEND\t',
            'INPUT': outputs['JoinAttributesByFieldValueBsa1300_area']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPgs_ratio_1300'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(267)
        if feedback.isCanceled():
            return {}

        # NDVI_SA100 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_SA100'],
            'FIELD_2': parameters['idfield'],
            'INPUT': parameters['indivualsgeolocation'],
            'INPUT_2': outputs['Ndvi_sa100RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa100JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(268)
        if feedback.isCanceled():
            return {}

        # NDVI_SA400 Rename field
        alg_params = {
            'FIELD': 'VALUE_mean',
            'INPUT': outputs['Ndvi_sa400JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'NDVI_SA400',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa400RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(269)
        if feedback.isCanceled():
            return {}

        # GS_uses_div_BSA1200_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_div_BSA1200',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'if( "GS_play_BSA1200" > 0, 1, 0) +  if( "GS_sports_BSA1200" > 0, 1, 0) + if( "GS_walk_BSA1200" > 0, 1, 0) + if( "GS_gard_BSA1200" > 0, 1, 0) +  if( "GS_social_BSA1200" > 0, 1, 0) +  if( "GS_other_BSA1200" > 0, 1, 0)',
            'INPUT': outputs['Gs_uses_sum_bsa1200_fieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_div_bsa1200_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(270)
        if feedback.isCanceled():
            return {}

        # GS_social_BSA600_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_social_BSA600',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_gard_bsa600_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_social_bsa600_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(271)
        if feedback.isCanceled():
            return {}

        # Field calculator PGS_ratio_1200
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_ratio_1200',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'CASE\n\tWHEN "PGS_in_SA1200" = NULL THEN 0\n\tELSE "PGS_in_SA1200"/"area"\nEND\t',
            'INPUT': outputs['JoinAttributesByFieldValueBsa1200_area']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPgs_ratio_1200'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(272)
        if feedback.isCanceled():
            return {}

        # Field calculator PGS_ratio_1000
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_ratio_1000',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'CASE\n\tWHEN "PGS_in_SA1000" = NULL THEN 0\n\tELSE "PGS_in_SA1000"/"area"\nEND\t',
            'INPUT': outputs['JoinAttributesByFieldValueBsa1000_area']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPgs_ratio_1000'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(273)
        if feedback.isCanceled():
            return {}

        # GS_gard_BSA1500_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_gard_BSA1500',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_walk_bsa1500_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_gard_bsa1500_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(274)
        if feedback.isCanceled():
            return {}

        # GS_other_BSA700_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_other_BSA700',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_social_bsa700_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_other_bsa700_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(275)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA100 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA100'],
            'FIELD_2': parameters['idfield'],
            'INPUT': parameters['indivualsgeolocation'],
            'INPUT_2': outputs['Pgs_in_sa100FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa100JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(276)
        if feedback.isCanceled():
            return {}

        # Field calculator PGS_ratio_900
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_ratio_900',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'CASE\n\tWHEN "PGS_in_SA900" = NULL THEN 0\n\tELSE "PGS_in_SA900"/"area"\nEND\t',
            'INPUT': outputs['JoinAttributesByFieldValueBsa900_area']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPgs_ratio_900'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(277)
        if feedback.isCanceled():
            return {}

        # GS_other_BSA800_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_other_BSA800',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_social_bsa800_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_other_bsa800_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(278)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value BSA400_area
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA400'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['FieldCalculatorBsa400']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa400FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueBsa400_area'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(279)
        if feedback.isCanceled():
            return {}

        # GS_other_BSA1000_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_other_BSA1000',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_social_bsa1000_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_other_bsa1000_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(280)
        if feedback.isCanceled():
            return {}

        # Field calculator PGS_ratio_700
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_ratio_700',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'CASE\n\tWHEN "PGS_in_SA700" = NULL THEN 0\n\tELSE "PGS_in_SA700"/"area"\nEND\t',
            'INPUT': outputs['JoinAttributesByFieldValueBsa700_area']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPgs_ratio_700'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(281)
        if feedback.isCanceled():
            return {}

        # GS_gard_BSA100_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_gard_BSA100',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_walk_bsa100_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_gard_bsa100_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(282)
        if feedback.isCanceled():
            return {}

        # GS_walk_BSA900_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_walk_BSA900',
            'POINTS': parameters['pgs (2) (4) (2) (2)'],
            'POLYGONS': outputs['Gs_sports_bsa900_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_walk_bsa900_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(283)
        if feedback.isCanceled():
            return {}

        # GS_social_BSA1100_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_social_BSA1100',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_gard_bsa1100_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_social_bsa1100_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(284)
        if feedback.isCanceled():
            return {}

        # GS_other_BSA600_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_other_BSA600',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_social_bsa600_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_other_bsa600_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(285)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA200 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA200'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_in_sa100JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa200FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa200JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(286)
        if feedback.isCanceled():
            return {}

        # Field calculator PGS_ratio_400
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_ratio_400',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'CASE\n\tWHEN "PGS_in_SA400" = NULL THEN 0\n\tELSE "PGS_in_SA400"/"area"\nEND\t',
            'INPUT': outputs['JoinAttributesByFieldValueBsa400_area']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPgs_ratio_400'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(287)
        if feedback.isCanceled():
            return {}

        # Field calculator PGS_ratio_300
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_ratio_300',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'CASE\n\tWHEN "PGS_in_SA300" = NULL THEN 0\n\tELSE "PGS_in_SA300"/"area"\nEND\t',
            'INPUT': outputs['JoinAttributesByFieldValueBsa300_area']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPgs_ratio_300'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(288)
        if feedback.isCanceled():
            return {}

        # GS_uses_sum_BSA600_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_sum_BSA600',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"GS_play_BSA600" + "GS_sports_BSA600" + "GS_walk_BSA600" + "GS_gard_BSA600" + "GS_social_BSA600" + "GS_other_BSA600"',
            'INPUT': outputs['Gs_other_bsa600_countPointsInPolygon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_sum_bsa600_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(289)
        if feedback.isCanceled():
            return {}

        # NDVI_B200 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_B200'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_b100JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_b200RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b200JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(290)
        if feedback.isCanceled():
            return {}

        # GS_gard_BSA1400_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_gard_BSA1400',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_walk_bsa1400_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_gard_bsa1400_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(291)
        if feedback.isCanceled():
            return {}

        # GS_other_BSA1100_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_other_BSA1100',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_social_bsa1100_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_other_bsa1100_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(292)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA300 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA300'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_in_sa200JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa300FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa300JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(293)
        if feedback.isCanceled():
            return {}

        # GS_gard_BSA500_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_gard_BSA500',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_walk_bsa500_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_gard_bsa500_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(294)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value BSA600_area
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA600'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['FieldCalculatorBsa600']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa600FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueBsa600_area'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(295)
        if feedback.isCanceled():
            return {}

        # NDVI_SA200 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_SA200'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_sa100JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_sa200RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa200JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(296)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value BSA500_area
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA500'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['FieldCalculatorBsa500']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa500FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueBsa500_area'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(297)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA200 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_A2_SA200'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_a2_sa100JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_a2_sa200RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa200JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(298)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1500 Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_in_SA1500',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': ' $area ',
            'INPUT': outputs['Pgs_in_sa1500Clip']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1500FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(299)
        if feedback.isCanceled():
            return {}

        # GS_sports_BSA400_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_sports_BSA400',
            'POINTS': parameters['pgs (2) (4) (2)'],
            'POLYGONS': outputs['Gs_play_bsa400_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_sports_bsa400_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(300)
        if feedback.isCanceled():
            return {}

        # GS_uses_sum_BSA700_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_sum_BSA700',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"GS_play_BSA700" + "GS_sports_BSA700" + "GS_walk_BSA700" + "GS_gard_BSA700" + "GS_social_BSA700" + "GS_other_BSA700"',
            'INPUT': outputs['Gs_other_bsa700_countPointsInPolygon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_sum_bsa700_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(301)
        if feedback.isCanceled():
            return {}

        # GS_walk_BSA300_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_walk_BSA300',
            'POINTS': parameters['pgs (2) (4) (2) (2)'],
            'POLYGONS': outputs['Gs_sports_bsa300_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_walk_bsa300_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(302)
        if feedback.isCanceled():
            return {}

        # GS_gard_BSA900_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_gard_BSA900',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_walk_bsa900_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_gard_bsa900_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(303)
        if feedback.isCanceled():
            return {}

        # GS_social_BSA1500_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_social_BSA1500',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_gard_bsa1500_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_social_bsa1500_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(304)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA400 Rename field
        alg_params = {
            'FIELD': 'PGS_area_sum',
            'INPUT': outputs['Pgs_a2_sa400JoinAttributesByLocationSummary']['OUTPUT'],
            'NEW_NAME': 'PGS_A2_SA400',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa400RenameField'] = processing.run('native:renametablefield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(305)
        if feedback.isCanceled():
            return {}

        # GS_uses_sum_BSA1000_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_sum_BSA1000',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"GS_play_BSA1000" + "GS_sports_BSA1000" + "GS_walk_BSA1000" + "GS_gard_BSA1000" + "GS_social_BSA1000" + "GS_other_BSA1000"',
            'INPUT': outputs['Gs_other_bsa1000_countPointsInPolygon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_sum_bsa1000_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(306)
        if feedback.isCanceled():
            return {}

        # GS_uses_div_BSA600_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_div_BSA600',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'if( "GS_play_BSA600" > 0, 1, 0) +  if( "GS_sports_BSA600" > 0, 1, 0) + if( "GS_walk_BSA600" > 0, 1, 0) + if( "GS_gard_BSA600" > 0, 1, 0) +  if( "GS_social_BSA600" > 0, 1, 0) +  if( "GS_other_BSA600" > 0, 1, 0)',
            'INPUT': outputs['Gs_uses_sum_bsa600_fieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_div_bsa600_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(307)
        if feedback.isCanceled():
            return {}

        # Field calculator PGS_ratio_200
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_ratio_200',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'CASE\n\tWHEN "PGS_in_SA200" = NULL THEN 0\n\tELSE "PGS_in_SA200"/"area"\nEND\t\n\t',
            'INPUT': outputs['JoinAttributesByFieldValueBsa200_area']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPgs_ratio_200'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(308)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value BSA1500_area
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA1500'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['FieldCalculatorBsa1500']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa1500FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueBsa1500_area'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(309)
        if feedback.isCanceled():
            return {}

        # GS_uses_sum_BSA1100_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_sum_BSA1100',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"GS_play_BSA1100" + "GS_sports_BSA1100" + "GS_walk_BSA1100" + "GS_gard_BSA1100" + "GS_social_BSA1100" + "GS_other_BSA1100"',
            'INPUT': outputs['Gs_other_bsa1100_countPointsInPolygon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_sum_bsa1100_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(310)
        if feedback.isCanceled():
            return {}

        # GS_other_BSA1500_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_other_BSA1500',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_social_bsa1500_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_other_bsa1500_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(311)
        if feedback.isCanceled():
            return {}

        # GS_uses_sum_BSA1300_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_sum_BSA1300',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"GS_play_BSA1300" + "GS_sports_BSA1300" + "GS_walk_BSA1300" + "GS_gard_BSA1300" + "GS_social_BSA1300" + "GS_other_BSA1300"',
            'INPUT': outputs['Gs_other_bsa1300_countPointsInPolygon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_sum_bsa1300_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(312)
        if feedback.isCanceled():
            return {}

        # GS_social_BSA100_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_social_BSA100',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_gard_bsa100_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_social_bsa100_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(313)
        if feedback.isCanceled():
            return {}

        # NDVI_B300 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_B300'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_b200JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_b300RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b300JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(314)
        if feedback.isCanceled():
            return {}

        # GS_social_BSA500_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_social_BSA500',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_gard_bsa500_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_social_bsa500_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(315)
        if feedback.isCanceled():
            return {}

        # Field calculator PGS_ratio_1500
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_ratio_1500',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'CASE\n\tWHEN "PGS_in_SA1500" = NULL THEN 0\n\tELSE "PGS_in_SA1500"/"area"\nEND\t',
            'INPUT': outputs['JoinAttributesByFieldValueBsa1500_area']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPgs_ratio_1500'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(316)
        if feedback.isCanceled():
            return {}

        # GS_social_BSA200_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_social_BSA200',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_gard_bsa200_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_social_bsa200_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(317)
        if feedback.isCanceled():
            return {}

        # GS_social_BSA1400_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_social_BSA1400',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_gard_bsa1400_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_social_bsa1400_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(318)
        if feedback.isCanceled():
            return {}

        # Field calculator PGS_ratio_500
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_ratio_500',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'CASE\n\tWHEN "PGS_in_SA500" = NULL THEN 0\n\tELSE "PGS_in_SA500"/"area"\nEND\t',
            'INPUT': outputs['JoinAttributesByFieldValueBsa500_area']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPgs_ratio_500'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(319)
        if feedback.isCanceled():
            return {}

        # NDVI_SA300 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_SA300'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_sa200JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_sa300RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa300JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(320)
        if feedback.isCanceled():
            return {}

        # GS_uses_sum_BSA800_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_sum_BSA800',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"GS_play_BSA800" + "GS_sports_BSA800" + "GS_walk_BSA800" + "GS_gard_BSA800" + "GS_social_BSA800" + "GS_other_BSA800"',
            'INPUT': outputs['Gs_other_bsa800_countPointsInPolygon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_sum_bsa800_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(321)
        if feedback.isCanceled():
            return {}

        # GS_social_BSA900_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_social_BSA900',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_gard_bsa900_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_social_bsa900_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(322)
        if feedback.isCanceled():
            return {}

        # GS_uses_sum_BSA1500_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_sum_BSA1500',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"GS_play_BSA1500" + "GS_sports_BSA1500" + "GS_walk_BSA1500" + "GS_gard_BSA1500" + "GS_social_BSA1500" + "GS_other_BSA1500"',
            'INPUT': outputs['Gs_other_bsa1500_countPointsInPolygon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_sum_bsa1500_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(323)
        if feedback.isCanceled():
            return {}

        # GS_other_BSA1400_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_other_BSA1400',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_social_bsa1400_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_other_bsa1400_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(324)
        if feedback.isCanceled():
            return {}

        # GS_other_BSA900_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_other_BSA900',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_social_bsa900_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_other_bsa900_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(325)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA400 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA400'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_in_sa300JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa400FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa400JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(326)
        if feedback.isCanceled():
            return {}

        # GS_uses_div_BSA1100_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_div_BSA1100',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'if( "GS_play_BSA1100" > 0, 1, 0) +  if( "GS_sports_BSA1100" > 0, 1, 0) + if( "GS_walk_BSA1100" > 0, 1, 0) + if( "GS_gard_BSA1100" > 0, 1, 0) +  if( "GS_social_BSA1100" > 0, 1, 0) +  if( "GS_other_BSA1100" > 0, 1, 0)',
            'INPUT': outputs['Gs_uses_sum_bsa1100_fieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_div_bsa1100_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(327)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA300 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_A2_SA300'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_a2_sa200JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_a2_sa300RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa300JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(328)
        if feedback.isCanceled():
            return {}

        # NDVI_B400 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_B400'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_b300JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_b400RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b400JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(329)
        if feedback.isCanceled():
            return {}

        # GS_walk_BSA400_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_walk_BSA400',
            'POINTS': parameters['pgs (2) (4) (2) (2)'],
            'POLYGONS': outputs['Gs_sports_bsa400_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_walk_bsa400_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(330)
        if feedback.isCanceled():
            return {}

        # GS_uses_div_BSA700_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_div_BSA700',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'if( "GS_play_BSA700" > 0, 1, 0) +  if( "GS_sports_BSA700" > 0, 1, 0) + if( "GS_walk_BSA700" > 0, 1, 0) + if( "GS_gard_BSA700" > 0, 1, 0) +  if( "GS_social_BSA700" > 0, 1, 0) +  if( "GS_other_BSA700" > 0, 1, 0)',
            'INPUT': outputs['Gs_uses_sum_bsa700_fieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_div_bsa700_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(331)
        if feedback.isCanceled():
            return {}

        # GS_gard_BSA300_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_gard_BSA300',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_walk_bsa300_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_gard_bsa300_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(332)
        if feedback.isCanceled():
            return {}

        # Field calculator PGS_ratio_600
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_ratio_600',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'CASE\n\tWHEN "PGS_in_SA600" = NULL THEN 0\n\tELSE "PGS_in_SA600"/"area"\nEND\t',
            'INPUT': outputs['JoinAttributesByFieldValueBsa600_area']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPgs_ratio_600'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(333)
        if feedback.isCanceled():
            return {}

        # GS_social_BSA300_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_social_BSA300',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_gard_bsa300_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_social_bsa300_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(334)
        if feedback.isCanceled():
            return {}

        # GS_uses_div_BSA800_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_div_BSA800',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'if( "GS_play_BSA800" > 0, 1, 0) +  if( "GS_sports_BSA800" > 0, 1, 0) + if( "GS_walk_BSA800" > 0, 1, 0) + if( "GS_gard_BSA800" > 0, 1, 0) +  if( "GS_social_BSA800" > 0, 1, 0) +  if( "GS_other_BSA800" > 0, 1, 0)',
            'INPUT': outputs['Gs_uses_sum_bsa800_fieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_div_bsa800_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(335)
        if feedback.isCanceled():
            return {}

        # GS_uses_div_BSA1500_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_div_BSA1500',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'if( "GS_play_BSA1500" > 0, 1, 0) +  if( "GS_sports_BSA1500" > 0, 1, 0) + if( "GS_walk_BSA1500" > 0, 1, 0) + if( "GS_gard_BSA1500" > 0, 1, 0) +  if( "GS_social_BSA1500" > 0, 1, 0) +  if( "GS_other_BSA1500" > 0, 1, 0)',
            'INPUT': outputs['Gs_uses_sum_bsa1500_fieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_div_bsa1500_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(336)
        if feedback.isCanceled():
            return {}

        # GS_uses_sum_BSA1400_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_sum_BSA1400',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"GS_play_BSA1400" + "GS_sports_BSA1400" + "GS_walk_BSA1400" + "GS_gard_BSA1400" + "GS_social_BSA1400" + "GS_other_BSA1400"',
            'INPUT': outputs['Gs_other_bsa1400_countPointsInPolygon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_sum_bsa1400_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(337)
        if feedback.isCanceled():
            return {}

        # GS_gard_BSA400_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_gard_BSA400',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_walk_bsa400_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_gard_bsa400_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(338)
        if feedback.isCanceled():
            return {}

        # GS_uses_div_BSA1000_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_div_BSA1000',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'if( "GS_play_BSA1000" > 0, 1, 0) +  if( "GS_sports_BSA1000" > 0, 1, 0) + if( "GS_walk_BSA1000" > 0, 1, 0) + if( "GS_gard_BSA1000" > 0, 1, 0) +  if( "GS_social_BSA1000" > 0, 1, 0) +  if( "GS_other_BSA1000" > 0, 1, 0)',
            'INPUT': outputs['Gs_uses_sum_bsa1000_fieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_div_bsa1000_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(339)
        if feedback.isCanceled():
            return {}

        # NDVI_B500 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_B500'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_b400JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_b500RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b500JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(340)
        if feedback.isCanceled():
            return {}

        # GS_social_BSA400_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_social_BSA400',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_gard_bsa400_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_social_bsa400_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(341)
        if feedback.isCanceled():
            return {}

        # GS_uses_sum_BSA900_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_sum_BSA900',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"GS_play_BSA900" + "GS_sports_BSA900" + "GS_walk_BSA900" + "GS_gard_BSA900" + "GS_social_BSA900" + "GS_other_BSA900"',
            'INPUT': outputs['Gs_other_bsa900_countPointsInPolygon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_sum_bsa900_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(342)
        if feedback.isCanceled():
            return {}

        # GS_uses_div_BSA1300_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_div_BSA1300',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'if( "GS_play_BSA1300" > 0, 1, 0) +  if( "GS_sports_BSA1300" > 0, 1, 0) + if( "GS_walk_BSA1300" > 0, 1, 0) + if( "GS_gard_BSA1300" > 0, 1, 0) +  if( "GS_social_BSA1300" > 0, 1, 0) +  if( "GS_other_BSA1300" > 0, 1, 0)',
            'INPUT': outputs['Gs_uses_sum_bsa1300_fieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_div_bsa1300_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(343)
        if feedback.isCanceled():
            return {}

        # GS_other_BSA500_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_other_BSA500',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_social_bsa500_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_other_bsa500_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(344)
        if feedback.isCanceled():
            return {}

        # GS_other_BSA100_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_other_BSA100',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_social_bsa100_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_other_bsa100_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(345)
        if feedback.isCanceled():
            return {}

        # NDVI_SA400 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_SA400'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_sa300JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_sa400RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa400JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(346)
        if feedback.isCanceled():
            return {}

        # GS_other_BSA400_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_other_BSA400',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_social_bsa400_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_other_bsa400_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(347)
        if feedback.isCanceled():
            return {}

        # GS_other_BSA200_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_other_BSA200',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_social_bsa200_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_other_bsa200_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(348)
        if feedback.isCanceled():
            return {}

        # GS_other_BSA300_Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'GS_other_BSA300',
            'POINTS': parameters['pgs (2) (4) (2) (2) (2) (2) (2)'],
            'POLYGONS': outputs['Gs_social_bsa300_countPointsInPolygon']['OUTPUT'],
            'WEIGHT': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_other_bsa300_countPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(349)
        if feedback.isCanceled():
            return {}

        # GS_uses_sum_BSA300_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_sum_BSA300',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"GS_play_BSA300" + "GS_sports_BSA300" + "GS_walk_BSA300" + "GS_gard_BSA300" + "GS_social_BSA300" + "GS_other_BSA300"',
            'INPUT': outputs['Gs_other_bsa300_countPointsInPolygon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_sum_bsa300_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(350)
        if feedback.isCanceled():
            return {}

        # GS_uses_sum_BSA100_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_sum_BSA100',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"GS_play_BSA100" + "GS_sports_BSA100" + "GS_walk_BSA100" + "GS_gard_BSA100" + "GS_social_BSA100" + "GS_other_BSA100"',
            'INPUT': outputs['Gs_other_bsa100_countPointsInPolygon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_sum_bsa100_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(351)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA500 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA500'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_in_sa400JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa500FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa500JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(352)
        if feedback.isCanceled():
            return {}

        # GS_uses_div_BSA900_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_div_BSA900',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'if( "GS_play_BSA900" > 0, 1, 0) +  if( "GS_sports_BSA900" > 0, 1, 0) + if( "GS_walk_BSA900" > 0, 1, 0) + if( "GS_gard_BSA900" > 0, 1, 0) +  if( "GS_social_BSA900" > 0, 1, 0) +  if( "GS_other_BSA900" > 0, 1, 0)',
            'INPUT': outputs['Gs_uses_sum_bsa900_fieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_div_bsa900_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(353)
        if feedback.isCanceled():
            return {}

        # NDVI_B600 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_B600'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_b500JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_b600RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b600JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(354)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA400 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_A2_SA400'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_a2_sa300JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_a2_sa400RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa400JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(355)
        if feedback.isCanceled():
            return {}

        # GS_uses_sum_BSA200_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_sum_BSA200',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"GS_play_BSA200" + "GS_sports_BSA200" + "GS_walk_BSA200" + "GS_gard_BSA200" + "GS_social_BSA200" + "GS_other_BSA200"',
            'INPUT': outputs['Gs_other_bsa200_countPointsInPolygon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_sum_bsa200_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(356)
        if feedback.isCanceled():
            return {}

        # GS_uses_div_BSA1400_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_div_BSA1400',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'if( "GS_play_BSA1400" > 0, 1, 0) +  if( "GS_sports_BSA1400" > 0, 1, 0) + if( "GS_walk_BSA1400" > 0, 1, 0) + if( "GS_gard_BSA1400" > 0, 1, 0) +  if( "GS_social_BSA1400" > 0, 1, 0) +  if( "GS_other_BSA1400" > 0, 1, 0)',
            'INPUT': outputs['Gs_uses_sum_bsa1400_fieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_div_bsa1400_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(357)
        if feedback.isCanceled():
            return {}

        # GS_uses_sum_BSA400_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_sum_BSA400',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"GS_play_BSA400" + "GS_sports_BSA400" + "GS_walk_BSA400" + "GS_gard_BSA400" + "GS_social_BSA400" + "GS_other_BSA400"',
            'INPUT': outputs['Gs_other_bsa400_countPointsInPolygon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_sum_bsa400_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(358)
        if feedback.isCanceled():
            return {}

        # GS_uses_div_BSA200_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_div_BSA200',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'if( "GS_play_BSA200" > 0, 1, 0) +  if( "GS_sports_BSA200" > 0, 1, 0) + if( "GS_walk_BSA200" > 0, 1, 0) + if( "GS_gard_BSA200" > 0, 1, 0) +  if( "GS_social_BSA200" > 0, 1, 0) +  if( "GS_other_BSA200" > 0, 1, 0)',
            'INPUT': outputs['Gs_uses_sum_bsa200_fieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_div_bsa200_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(359)
        if feedback.isCanceled():
            return {}

        # NDVI_SA500 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_SA500'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_sa400JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_sa500RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa500JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(360)
        if feedback.isCanceled():
            return {}

        # GS_uses_div_BSA300_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_div_BSA300',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'if( "GS_play_BSA300" > 0, 1, 0) +  if( "GS_sports_BSA300" > 0, 1, 0) + if( "GS_walk_BSA300" > 0, 1, 0) + if( "GS_gard_BSA300" > 0, 1, 0) +  if( "GS_social_BSA300" > 0, 1, 0) +  if( "GS_other_BSA300" > 0, 1, 0)',
            'INPUT': outputs['Gs_uses_sum_bsa300_fieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_div_bsa300_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(361)
        if feedback.isCanceled():
            return {}

        # GS_uses_div_BSA400_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_div_BSA400',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'if( "GS_play_BSA400" > 0, 1, 0) +  if( "GS_sports_BSA400" > 0, 1, 0) + if( "GS_walk_BSA400" > 0, 1, 0) + if( "GS_gard_BSA400" > 0, 1, 0) +  if( "GS_social_BSA400" > 0, 1, 0) +  if( "GS_other_BSA400" > 0, 1, 0)',
            'INPUT': outputs['Gs_uses_sum_bsa400_fieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_div_bsa400_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(362)
        if feedback.isCanceled():
            return {}

        # GS_uses_div_BSA100_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_div_BSA100',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'if( "GS_play_BSA100" > 0, 1, 0) +  if( "GS_sports_BSA100" > 0, 1, 0) + if( "GS_walk_BSA100" > 0, 1, 0) + if( "GS_gard_BSA100" > 0, 1, 0) +  if( "GS_social_BSA100" > 0, 1, 0) +  if( "GS_other_BSA100" > 0, 1, 0)',
            'INPUT': outputs['Gs_uses_sum_bsa100_fieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_div_bsa100_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(363)
        if feedback.isCanceled():
            return {}

        # NDVI_SA600 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_SA600'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_sa500JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_sa600RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa600JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(364)
        if feedback.isCanceled():
            return {}

        # GS_uses_sum_BSA500_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_sum_BSA500',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': '"GS_play_BSA500" + "GS_sports_BSA500" + "GS_walk_BSA500" + "GS_gard_BSA500" + "GS_social_BSA500" + "GS_other_BSA500"',
            'INPUT': outputs['Gs_other_bsa500_countPointsInPolygon']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_sum_bsa500_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(365)
        if feedback.isCanceled():
            return {}

        # NDVI_SA700 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_SA700'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_sa600JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_sa700RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa700JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(366)
        if feedback.isCanceled():
            return {}

        # NDVI_B700 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_B700'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_b600JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_b700RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b700JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(367)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA500 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_A2_SA500'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_a2_sa400JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_a2_sa500RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa500JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(368)
        if feedback.isCanceled():
            return {}

        # NDVI_B800 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_B800'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_b700JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_b800RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b800JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(369)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA600 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA600'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_in_sa500JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa600FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa600JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(370)
        if feedback.isCanceled():
            return {}

        # GS_uses_BSA100 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['GS_uses_sum_BSA100','GS_uses_div_BSA100'],
            'FIELD_2': parameters['idfield'],
            'INPUT': parameters['indivualsgeolocation'],
            'INPUT_2': outputs['Gs_uses_div_bsa100_fieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_bsa100JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(371)
        if feedback.isCanceled():
            return {}

        # GS_uses_div_BSA500_Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GS_uses_div_BSA500',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'if( "GS_play_BSA500" > 0, 1, 0) +  if( "GS_sports_BSA500" > 0, 1, 0) + if( "GS_walk_BSA500" > 0, 1, 0) + if( "GS_gard_BSA500" > 0, 1, 0) +  if( "GS_social_BSA500" > 0, 1, 0) +  if( "GS_other_BSA500" > 0, 1, 0)',
            'INPUT': outputs['Gs_uses_sum_bsa500_fieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_div_bsa500_fieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(372)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA600 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_A2_SA600'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_a2_sa500JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_a2_sa600RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa600JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(373)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA700 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA700'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_in_sa600JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa700FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa700JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(374)
        if feedback.isCanceled():
            return {}

        # NDVI_SA800 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_SA800'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_sa700JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_sa800RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa800JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(375)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA700 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_A2_SA700'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_a2_sa600JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_a2_sa700RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa700JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(376)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA800 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA800'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_in_sa700JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa800FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa800JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(377)
        if feedback.isCanceled():
            return {}

        # GS_uses_BSA200 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['GS_uses_sum_BSA200','GS_uses_div_BSA200'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Gs_uses_bsa100JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Gs_uses_div_bsa200_fieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_bsa200JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(378)
        if feedback.isCanceled():
            return {}

        # NDVI_B900 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_B900'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_b800JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_b900RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b900JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(379)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA900 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA900'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_in_sa800JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa900FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa900JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(380)
        if feedback.isCanceled():
            return {}

        # NDVI_SA900 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_SA900'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_sa800JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_sa900RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa900JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(381)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA800 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_A2_SA800'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_a2_sa700JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_a2_sa800RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa800JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(382)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1000 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA1000'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_in_sa900JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa1000FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1000JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(383)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA900 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_A2_SA900'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_a2_sa800JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_a2_sa900RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa900JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(384)
        if feedback.isCanceled():
            return {}

        # GS_uses_BSA300 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['GS_uses_sum_BSA300','GS_uses_div_BSA300'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Gs_uses_bsa200JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Gs_uses_div_bsa300_fieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_bsa300JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(385)
        if feedback.isCanceled():
            return {}

        # NDVI_B1000 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_B1000'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_b900JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_b1000RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1000JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(386)
        if feedback.isCanceled():
            return {}

        # GS_uses_BSA400 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['GS_uses_sum_BSA400','GS_uses_div_BSA400'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Gs_uses_bsa300JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Gs_uses_div_bsa400_fieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_bsa400JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(387)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1000 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_A2_SA1000'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_a2_sa900JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_a2_sa1000RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1000JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(388)
        if feedback.isCanceled():
            return {}

        # GS_uses_BSA500 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['GS_uses_sum_BSA500','GS_uses_div_BSA500'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Gs_uses_bsa400JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Gs_uses_div_bsa500_fieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_bsa500JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(389)
        if feedback.isCanceled():
            return {}

        # NDVI_B1100 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_B1100'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_b1000JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_b1100RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1100JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(390)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1100 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA1100'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_in_sa1000JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa1100FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1100JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(391)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1000 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_SA1000'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_sa900JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_sa1000RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1000JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(392)
        if feedback.isCanceled():
            return {}

        # NDVI_B1200 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_B1200'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_b1100JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_b1200RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1200JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(393)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1100 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_A2_SA1100'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_a2_sa1000JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_a2_sa1100RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1100JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(394)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1100 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_SA1100'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_sa1000JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_sa1100RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1100JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(395)
        if feedback.isCanceled():
            return {}

        # GS_uses_BSA600 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['GS_uses_sum_BSA600','GS_uses_div_BSA600'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Gs_uses_bsa500JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Gs_uses_div_bsa600_fieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_bsa600JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(396)
        if feedback.isCanceled():
            return {}

        # NDVI_B1300 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_B1300'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_b1200JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_b1300RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1300JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(397)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1200 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_A2_SA1200'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_a2_sa1100JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_a2_sa1200RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1200JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(398)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1200 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA1200'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_in_sa1100JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa1200FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1200JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(399)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1200 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_SA1200'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_sa1100JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_sa1200RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1200JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(400)
        if feedback.isCanceled():
            return {}

        # GS_uses_BSA700 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['GS_uses_sum_BSA700','GS_uses_div_BSA700'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Gs_uses_bsa600JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Gs_uses_div_bsa700_fieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_bsa700JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(401)
        if feedback.isCanceled():
            return {}

        # GS_uses_BSA800 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['GS_uses_sum_BSA800','GS_uses_div_BSA800'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Gs_uses_bsa700JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Gs_uses_div_bsa800_fieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_bsa800JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(402)
        if feedback.isCanceled():
            return {}

        # NDVI_B1400 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_B1400'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_b1300JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_b1400RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_b1400JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(403)
        if feedback.isCanceled():
            return {}

        # NDVI_B1500 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_B1500'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_b1400JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_b1500RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['NdviAroundAResidentialAdressMeanWithinBuffer']
        }
        outputs['Ndvi_b1500JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['NdviAroundAResidentialAdressMeanWithinBuffer'] = outputs['Ndvi_b1500JoinAttributesByFieldValue']['OUTPUT']

        feedback.setCurrentStep(404)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1300 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA1300'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_in_sa1200JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa1300FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1300JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(405)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1400 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA1400'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_in_sa1300JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa1400FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1400JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(406)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1300 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_SA1300'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_sa1200JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_sa1300RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1300JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(407)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1300 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_A2_SA1300'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_a2_sa1200JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_a2_sa1300RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1300JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(408)
        if feedback.isCanceled():
            return {}

        # GS_uses_BSA900 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['GS_uses_sum_BSA900','GS_uses_div_BSA900'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Gs_uses_bsa800JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Gs_uses_div_bsa900_fieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_bsa900JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(409)
        if feedback.isCanceled():
            return {}

        # GS_uses_BSA1000 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['GS_uses_sum_BSA1000','GS_uses_div_BSA1000'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Gs_uses_bsa900JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Gs_uses_div_bsa1000_fieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_bsa1000JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(410)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1400 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_SA1400'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_sa1300JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_sa1400RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ndvi_sa1400JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(411)
        if feedback.isCanceled():
            return {}

        # PGS_in_SA1500 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_in_SA1500'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_in_sa1400JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_in_sa1500FieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_in_sa1500JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(412)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1400 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_A2_SA1400'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_a2_sa1300JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_a2_sa1400RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Pgs_a2_sa1400JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(413)
        if feedback.isCanceled():
            return {}

        # GS_uses_BSA1100 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['GS_uses_sum_BSA1100','GS_uses_div_BSA1100'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Gs_uses_bsa1000JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Gs_uses_div_bsa1100_fieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_bsa1100JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(414)
        if feedback.isCanceled():
            return {}

        # PGS_A2_SA1500 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_A2_SA1500'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Pgs_a2_sa1400JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Pgs_a2_sa1500RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['PublicGreenSpaceAccessibleWithinNetworkDistanceM2ThatIntersectWithBsa']
        }
        outputs['Pgs_a2_sa1500JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['PublicGreenSpaceAccessibleWithinNetworkDistanceM2ThatIntersectWithBsa'] = outputs['Pgs_a2_sa1500JoinAttributesByFieldValue']['OUTPUT']

        feedback.setCurrentStep(415)
        if feedback.isCanceled():
            return {}

        # Field calculator PGS_ACC
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'PGS_ACC',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'CASE \n  WHEN "PGS_in_SA100" > 0 THEN 100\n  WHEN "PGS_in_SA200" > 0 THEN 200\n  WHEN "PGS_in_SA300" > 0 THEN 300\n  WHEN "PGS_in_SA400" > 0 THEN 400\n  WHEN "PGS_in_SA500" > 0 THEN 500\n  WHEN "PGS_in_SA600" > 0 THEN 600\n  WHEN "PGS_in_SA700" > 0 THEN 700\n  WHEN "PGS_in_SA800" > 0 THEN 800\n  WHEN "PGS_in_SA900" > 0 THEN 900\n  WHEN "PGS_in_SA1000" > 0 THEN 1000\n  WHEN "PGS_in_SA1100" > 0 THEN 1100\n  WHEN "PGS_in_SA1200" > 0 THEN 1200\n  WHEN "PGS_in_SA1300" > 0 THEN 1300\n  WHEN "PGS_in_SA1400" > 0 THEN 1400\n  WHEN "PGS_in_SA1500" > 0 THEN 1500\n  ELSE NULL\nEND',
            'INPUT': outputs['Pgs_in_sa1500JoinAttributesByFieldValue']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPgs_acc'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(416)
        if feedback.isCanceled():
            return {}

        # NDVI_SA1500 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['NDVI_SA1500'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Ndvi_sa1400JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Ndvi_sa1500RenameField']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['NdviInNetworkDistanceMeanInBsa']
        }
        outputs['Ndvi_sa1500JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['NdviInNetworkDistanceMeanInBsa'] = outputs['Ndvi_sa1500JoinAttributesByFieldValue']['OUTPUT']

        feedback.setCurrentStep(417)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value PGS_ratio_100
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_ratio_100'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['FieldCalculatorPgs_acc']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorPgs_ratio_100']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValuePgs_ratio_100'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(418)
        if feedback.isCanceled():
            return {}

        # GS_uses_BSA1200 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['GS_uses_sum_BSA1200','GS_uses_div_BSA1200'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Gs_uses_bsa1100JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Gs_uses_div_bsa1200_fieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_bsa1200JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(419)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value PGS_ratio_200
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_ratio_200'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['JoinAttributesByFieldValuePgs_ratio_100']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorPgs_ratio_200']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValuePgs_ratio_200'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(420)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value PGS_ratio_300
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_ratio_300'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['JoinAttributesByFieldValuePgs_ratio_200']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorPgs_ratio_300']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValuePgs_ratio_300'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(421)
        if feedback.isCanceled():
            return {}

        # GS_uses_BSA1300 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['GS_uses_sum_BSA1300','GS_uses_div_BSA1300'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Gs_uses_bsa1200JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Gs_uses_div_bsa1300_fieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_bsa1300JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(422)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value PGS_ratio_400
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_ratio_400'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['JoinAttributesByFieldValuePgs_ratio_300']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorPgs_ratio_400']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValuePgs_ratio_400'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(423)
        if feedback.isCanceled():
            return {}

        # GS_uses_BSA1400 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['GS_uses_sum_BSA1400','GS_uses_div_BSA1400'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Gs_uses_bsa1300JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Gs_uses_div_bsa1400_fieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gs_uses_bsa1400JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(424)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value PGS_ratio_500
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_ratio_500'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['JoinAttributesByFieldValuePgs_ratio_400']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorPgs_ratio_500']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValuePgs_ratio_500'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(425)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value PGS_ratio_600
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_ratio_600'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['JoinAttributesByFieldValuePgs_ratio_500']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorPgs_ratio_600']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValuePgs_ratio_600'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(426)
        if feedback.isCanceled():
            return {}

        # GS_uses_BSA1500 Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['GS_uses_sum_BSA1500','GS_uses_div_BSA1500'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['Gs_uses_bsa1400JoinAttributesByFieldValue']['OUTPUT'],
            'INPUT_2': outputs['Gs_uses_div_bsa1500_fieldCalculator']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['GreenSpaceUsesWithinNetworkDistanceTotalSumAndDifferentUses']
        }
        outputs['Gs_uses_bsa1500JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['GreenSpaceUsesWithinNetworkDistanceTotalSumAndDifferentUses'] = outputs['Gs_uses_bsa1500JoinAttributesByFieldValue']['OUTPUT']

        feedback.setCurrentStep(427)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value PGS_ratio_700
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_ratio_700'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['JoinAttributesByFieldValuePgs_ratio_600']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorPgs_ratio_700']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValuePgs_ratio_700'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(428)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value PGS_ratio_800
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_ratio_800'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['JoinAttributesByFieldValuePgs_ratio_700']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorPgs_ratio_800']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValuePgs_ratio_800'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(429)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value PGS_ratio_900
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_ratio_900'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['JoinAttributesByFieldValuePgs_ratio_800']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorPgs_ratio_900']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValuePgs_ratio_900'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(430)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value PGS_ratio_1000
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_ratio_1000'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['JoinAttributesByFieldValuePgs_ratio_900']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorPgs_ratio_1000']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValuePgs_ratio_1000'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(431)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value PGS_ratio_1100
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_ratio_1100'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['JoinAttributesByFieldValuePgs_ratio_1000']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorPgs_ratio_1100']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValuePgs_ratio_1100'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(432)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value PGS_ratio_1200
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_ratio_1200'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['JoinAttributesByFieldValuePgs_ratio_1100']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorPgs_ratio_1200']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValuePgs_ratio_1200'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(433)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value PGS_ratio_1300
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_ratio_1300'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['JoinAttributesByFieldValuePgs_ratio_1200']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorPgs_ratio_1300']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValuePgs_ratio_1300'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(434)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value PGS_ratio_1400
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_ratio_1400'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['JoinAttributesByFieldValuePgs_ratio_1300']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorPgs_ratio_1400']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValuePgs_ratio_1400'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(435)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value PGS_ratio_1500
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['idfield'],
            'FIELDS_TO_COPY': ['PGS_ratio_1500'],
            'FIELD_2': parameters['idfield'],
            'INPUT': outputs['JoinAttributesByFieldValuePgs_ratio_1400']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorPgs_ratio_1500']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['PublicGreenSpaceWithinNetworkDistanceM2WithinBsa']
        }
        outputs['JoinAttributesByFieldValuePgs_ratio_1500'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['PublicGreenSpaceWithinNetworkDistanceM2WithinBsa'] = outputs['JoinAttributesByFieldValuePgs_ratio_1500']['OUTPUT']
        return results

    def name(self):
        return 'AID-PRIGSHARE'

    def displayName(self):
        return 'AID-PRIGSHARE'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def shortHelpString(self):
        return """<html><body><p>AID-PRIGSHARE.  Automazition of Indicator Development for Green Space Health Research in QGIS

The PRIGSHARE_QGIS_Script will produce green space and greenness indicators in distances from 100-1.500m every 100m automatically.

A frequent demand in the interdisciplinary field of green space health research is to reduce the effort to assess green space, especially for non-spatial disciplines. Realizing this issue, we developed AID-PRIGSHARE. AID-PRIGSHARE is an open-source script with an easy-to-use user interface that substantially reduces the time-intensive and complex task of green space indicator generation by automatization. AID-PRIGSHARE will simultaneously calculate indicators such as mean greenness, total public green space, access to green infrastructure, and green space uses for distances of 100-1500m in 100m steps around a (home) address if the input layers are provided. This substantially reduces the effort for sensitivity analysis and may provide support for research that aims to better understand the individual characteristics of green spaces and their effect range.

The script requires the input of addresses of individuals (point layer). Other inputs are only necessary for specific calculations (see input parameters below).</p>
<h2>Input parameters</h2>
<h3>Indivuals Geolocation</h3>
<p>Please provide a layer with the geolocation of the individuals of your study as a point layer. This will also be the layer, where all calculated spatial indicators will be added to the attribute table. 
Hint: Take care of potential bias. Often geolocation algorithms are not able to find all the addresses and place them in the city center instead. Harder to find are those addresses that are incorrectly identified. Both should be manually corrected before you use the algorithm.  </p>
<h3>ID_Field (identifier to seperate individuals in individual geolocation file)</h3>
<p>Please provide the exact name of the field in your individual geolocation point layer that is a unique identifier for each individual. </p>
<h3>Walkability Layer (Street Network)</h3>
<p>Needed for Accessibility Assessment / otherwise optional
Please provide a line layer with the street network.  </p>
<h3>Vegetation Index (needs to be vectorized)</h3>
<p>Needed for Vegetative Assessment / otherwise optional
Please provide a vectorized Vegetation Index polygon layer.  </p>
<h3>Public Green Space Layer</h3>
<p>Needed for Spatial Assessment / otherwise optional
Please provide a polygon layer with the public green spaces of your study area.  </p>
<h3>Semi-Public Green Spaces (will add SPGS indicator)</h3>
<p>Needed to calculate semi-public green spaces / otherwise optional.
Please provide a polygon layer with the lots of multi-story residential buildings derived from a cadastre map of your study area. 
If provided, the PRIGSHARE algorithm will add the indicator SPGS (Semi-Public Green Space) to the database for people living in these buildings. </p>
<h3>Private Green Space (will add PRGS indicator)</h3>
<p>Needed to calculate private green spaces / otherwise optional.
Please provide a polygon layer with the lots of one-family homes derived from a cadastre map of your study area. 
If provided, the PRIGSHARE algorithm will add the indicator PRGS (Private Green Space) to the database for people with a private garden. </p>
<h3>Buildings (will subtract building footprint from all green spaces if provided)</h3>
<p>Needed to calculate semi-public and private green spaces / otherwise optional.
Please provide a polygon layer with the building footprints of your study area.  </p>
<h3>Green Space Use 1</h3>
<p>Needed to assess the potential uses in green spaces around an individual / otherwise optional
Please provide a point layer with the green space uses of your study area. For example a point for every playground, fireplace, urban gardening, sports field, and maybe even walking entries in bigger parks as a proxy for the walkability they provide. 
If provided, the PRIGSHARE algorithm will add the indicators GS_uses and GS_diversity to the database for distances from 100m - 1500m. </p>
<br><p align="right">Algorithm author: will be added after peer-review</p><p align="right">Help author: will be added after peer-review</p><p align="right">Algorithm version: 1.0</p></body></html>"""

    def createInstance(self):
        return Aidprigshare()
