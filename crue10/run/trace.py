# coding: utf-8
from crue10.utils.crueconfigmetier import ENUM_SEVERITE
from crue10.utils import ExceptionCrue10
from crue10.utils.message import parse_message
from crue10.utils.settings import GRAVITE_AVERTISSEMENT, GRAVITE_MIN_ERROR


class Trace:
    """
    Trace
    - date
    - id
    - gravite
    - localisation_methode
    - localisation_fichier
    - localisation_ligne
    - nom_emh
    - parametres <str>: liste des paramètrse numérotés
    - gravite_int <int>: gravité (0=min, 100=max)

    Exemple d'une ligne contenant dans l'ordre les 7 premiers attributs de la trace (séparés par des ;) :
    2019-04-16T14:09:21.661;ID_VERSION;INFO;Crue10::EMHModeleBase::utiliserParametresSortiesService;EMHModeleBase.cpp;198;Mo_VS2013_c10_octobre_2014;"10";"2";"0";"1";"2"
    """
    def __init__(self, line):
        """
        :param line <str>: ligne d'un fichier CSV contenant des traces.
        Ex: 2019-04-16T14:09:21.661;ID_VERSION;INFO;Crue10::EMHModeleBase::utiliserParametresSortiesService;EMHModeleBase.cpp;198;Mo_VS2013_c10_octobre_2014;"10";"2";"0";"1";"2"
        """
        if not isinstance(line, str):
            line = line.encode('utf-8')  # Python2 fix: required to convert from unicode
        cells = line.replace('\n', '').replace('"', '').split(';')
        if len(cells) < 7:
            raise ExceptionCrue10("La trace ne contient pas assez de colonnes pour être lue :\n%s" % line)
        self.date, self.id, self.gravite, self.localisation_methode, self.localisation_fichier, \
            self.localisation_ligne, self.nom_emh = cells[:7]
        self.parametres = cells[7:]
        self.gravite_int = ENUM_SEVERITE[self.gravite]

    def is_erreur(self):
        gravite_min_int = ENUM_SEVERITE[GRAVITE_MIN_ERROR]
        return self.gravite_int <= gravite_min_int

    def is_avertissement(self):
        return self.gravite == GRAVITE_AVERTISSEMENT

    def get_message(self):
        return parse_message(self.id, self.nom_emh, self.parametres)

    def __repr__(self):
        return '%s|%s|%s|%s|%s'\
               % (self.date.ljust(23), self.gravite.ljust(6), self.nom_emh.ljust(32),
                  self.id.ljust(33), self.get_message())