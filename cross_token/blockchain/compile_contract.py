import os

from solcx import compile_source, install_solc
import json

from .utils.load_abi import load_local_abi
from .utils.load_bytecode import load_local_bytecode


def compile_the_contract():
    install_solc("0.8.0")

    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(dir_path + '/contracts/myToken.sol', 'r') as sol_file:
        sol_code = sol_file.read()

    compiled_sol = compile_source(sol_code)
    print('Successfully compiled myToken.sol')
    contract_interface = compiled_sol['<stdin>:myToken']

    with open(dir_path + '/contracts/myToken.abi', 'w') as abi_file:
        abi_file.write(json.dumps(contract_interface['abi']))

    with open(dir_path + '/contracts/myToken.bin', 'w') as abi_file:
        abi_file.write(json.dumps(contract_interface['bin']))

    print('Successfully saved abi and bytecode')
    return True


def is_contract_compiled():
    bc = load_local_bytecode()
    abi = load_local_abi()
    if all([bc, abi]):
        return True
    return False


if __name__ == '__main__':
    compile_the_contract()
