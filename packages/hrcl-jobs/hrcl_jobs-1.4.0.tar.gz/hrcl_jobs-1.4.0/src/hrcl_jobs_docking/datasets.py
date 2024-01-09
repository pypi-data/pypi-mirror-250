from dataclasses import dataclass
import numpy as np
import pandas as pd
import hrcl_jobs as hrcl
from mpi4py import MPI
from . import jobspec
from . import docking_inps

HIVE_PARAMS = {
    "mem_per_process": "60 gb",
    "num_omp_threads": 8,
}


def apnet_disco_dataset(
    db_path,
    table_name,
    col_check="apnet_totl_LIG",
    assay="KI",
    hex=False,
    check_apnet_errors=False,
    extra_info={},
    hive_params={
        "mem_per_process": "24 gb",
        "num_omp_threads": 4,
    },
):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    if hex:
        machine = hrcl.utils.machine_list_resources()
        memory_per_thread = f"{machine.memory_per_thread} gb"
        num_omp_threads = machine.omp_threads
    else:
        memory_per_thread = hive_params["mem_per_process"]
        num_omp_threads = hive_params["num_omp_threads"]
    print(f"{rank = } {memory_per_thread = } ")

    output_columns = [col_check]
    suffix = col_check.split("_")[1:]
    for i in ["apnet_elst", "apnet_exch", "apnet_indu", "apnet_disp"]:
        output_columns.append(i + "_" + "_".join(suffix))
    output_columns.append("apnet_errors")
    print(output_columns)

    matches = {
        col_check: ["NULL"],
        "Assay": [assay],
    }
    if check_apnet_errors:
        matches["apnet_errors"] = ["NULL"]

    con, cur = hrcl.sqlt.establish_connection(db_path)
    query = hrcl.sqlt.query_columns_for_values(
        cur,
        table_name,
        # id_names=["id", "PRO_PDB", "LIG_PDB", "WAT_PDB", "OTH_PDB"],
        id_names=["id"],
        matches=matches,
    )
    # query = [7916 ]

    hrcl.parallel.ms_sl_extra_info(
        id_list=query,
        db_path=db_path,
        table_name=table_name,
        js_obj=jobspec.apnet_disco_js,
        headers_sql=jobspec.apnet_disco_js_headers(),
        run_js_job=docking_inps.run_apnet_discos,
        extra_info=extra_info,
        ppm=memory_per_thread,
        id_label="id",
        output_columns=output_columns,
        print_insertion=True,
    )
    return

def vina_api_disco_dataset(
    db_path,
    table_name,
    col_check="vina_total_LIG",
    assay="KI",
    hex=False,
    check_apnet_errors=False,
    scoring_function="vina",
    extra_info={},
    hive_params={
        "mem_per_process": "24 gb",
        "num_omp_threads": 4,
    },
):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    if hex:
        machine = hrcl.utils.machine_list_resources()
        memory_per_thread = f"{machine.memory_per_thread} gb"
        num_omp_threads = machine.omp_threads
    else:
        memory_per_thread = hive_params["mem_per_process"]
        num_omp_threads = hive_params["num_omp_threads"]
    print(f"{rank = } {memory_per_thread = } ")

    output_columns = [col_check]
    suffix = col_check.split("__")[1:]
    for i in [
        f"{scoring_function}_inter",
        f"{scoring_function}_intra",
        f"{scoring_function}_torsion",
        f"{scoring_function}_best_pose",
        f"{scoring_function}_poses_pdbqt",
        f"{scoring_function}_all_poses",
        f"{scoring_function}_errors",
          ]:
        output_columns.append(i + "_" + "_".join(suffix))
    print(output_columns)

    matches = {
        col_check: ["NULL"],
        "Assay": [assay],
    }

    if check_apnet_errors:
        matches[f"{scoring_function}_errors_{suffix}"] = ["NULL"]

    con, cur = hrcl.sqlt.establish_connection(db_path)
    query = hrcl.sqlt.query_columns_for_values(
        cur,
        table_name,
        id_names=["id"],
        matches=matches,
    )

    extra_info['scoring_function'] = scoring_function
    # query = [7916 ]

    hrcl.parallel.ms_sl_extra_info(
        id_list=query,
        db_path=db_path,
        table_name=table_name,
        js_obj=jobspec.autodock_vina_disco_js,
        headers_sql=jobspec.autodock_vina_disco_js_headers(),
        run_js_job=docking_inps.run_apnet_discos,
        extra_info=extra_info,
        ppm=memory_per_thread,
        id_label="id",
        output_columns=output_columns,
        print_insertion=True,
    )
    return
