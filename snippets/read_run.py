import os.path
import sys

from crue10.run import RunResults
from crue10.utils import CrueError, logger


model_folder = '../../TatooineMesher_examples/VS2015/in/Etu_VS2015_conc'
rcal_path = os.path.join(model_folder,
                         'Runs/Sc_EtatsRef2015/R2019-04-16-14h09m19s/Mo_VS2013_c10_octobre_2014',
                         'VS2013_c10_EtatsRef.rcal.xml')
try:
    run = RunResults(rcal_path)
    print(run.summary())

    print(run.emh_types)  # 'Noeud', 'Casier'...
    print(run.emh)  # EMH identifiers list for every EMH type
    print(run.variables)  # Variable identifiers list for every EMH type

    # Read a single *steady* calculation
    res_perm = run.get_res_perm('Cc_360m3-s')
    for emh_type, res in res_perm.items():
        print(emh_type)
        print(res)  # shape = (number of EMHs, number of variables)

    # Read results at locations for all steady calculations
    #   shape = (number of steady calculations, number of requested EMH)
    print(run.get_res_all_perm_var_at_emhs('Z', ['St_RET33.300', 'Nd_VRH8.500']))

    # Create output folder if not existing
    out_folder = '../tmp/read_run'
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    # Export steady calculations data
    run.export_calc_perm_as_csv(os.path.join(out_folder, 'Etu_VS2015_conc_perms.csv'))

    # Read a single *unsteady* calculation
    res_trans = run.get_res_trans('Cc_Avr_2006')
    for emh_type, res in res_trans.items():
        print(emh_type)
        print(res)  # shape = (number of time steps, number of EMHs, number of variables)

    # Read results at locations for a single unsteady calculation
    #   shape = (number of time steps, number of requested EMHs)
    print(run.get_res_trans_var_at_emhs('Cc_Avr_2006', 'Z', ['St_RET33.300', 'Nd_VRH8.500']))

    # Export unsteady calculations data
    run.export_calc_trans_as_csv(os.path.join(out_folder, 'Etu_VS2015_conc_trans.csv'))

except CrueError as e:
    logger.critical(e)
    sys.exit(1)
