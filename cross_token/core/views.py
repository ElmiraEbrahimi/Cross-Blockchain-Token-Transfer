from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template import loader

from core.models import Config
from blockchain.compile_contract import compile_the_contract, is_contract_compiled
from blockchain.deploy import deploy_eth_contract, deploy_bsc_contract, contract_exists
from blockchain.functions import ContractFunctions


def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


# @login_required(login_url='/admin/')
def admin(request):
    # user = User.objects.get(username='admin')
    # if user != request.user:
    #     return JsonResponse({'error': 'user is not "admin". only admin can visit this page.'}, status=403)

    try:
        cf = ContractFunctions(is_bsc=False)
        eth_total_supply = cf.balance_of(cf.third_party_address)
    except Exception:
        eth_total_supply = 'Error: Could not establish connection to ETH blockchain.'

    try:
        cf = ContractFunctions(is_bsc=True)
        bsc_total_supply = cf.balance_of(cf.third_party_address)
    except Exception:
        bsc_total_supply = 'Error: Could not establish connection to BSC blockchain.'

    config = Config.objects.get()
    try:
        deployed_eth_contract_address = config.deployed_eth_contract_address
        is_eth_deployed = contract_exists(is_bsc=False, contract_address=deployed_eth_contract_address)
        config.is_eth_deployed = is_eth_deployed
    except Exception:
        is_eth_deployed = False
        config.is_eth_deployed = is_eth_deployed

    try:
        deployed_bsc_contract_address = config.deployed_bsc_contract_address
        is_bsc_deployed = contract_exists(is_bsc=True, contract_address=deployed_bsc_contract_address)
        config.is_bsc_deployed = is_bsc_deployed
    except Exception:
        is_bsc_deployed = False
        config.is_bsc_deployed = is_bsc_deployed

    is_compiled = is_contract_compiled()
    config.is_contract_compiled = is_compiled

    config.save()

    template = loader.get_template('admin.html')
    context = {
        'is_compiled': is_compiled,
        'is_eth_deployed': is_eth_deployed,
        'is_bsc_deployed': is_bsc_deployed,
        'eth_total_supply': eth_total_supply,
        'bsc_total_supply': bsc_total_supply,
    }
    return HttpResponse(template.render(context, request))


# @login_required(login_url='/admin/')
def alice(request):
    # user = User.objects.get(username='alice')
    # if user != request.user:
    #     return JsonResponse({'error': 'user is not "alice". only alice can visit this page.'}, status=403)

    alice_address = Config.objects.get().alice_eth_address
    if not alice_address:
        return JsonResponse({'error': 'Alice\'s ETH address is not specified in admin/'})

    try:
        cf = ContractFunctions(is_bsc=False)
        alice_balance = cf.balance_of(alice_address)
    except Exception as err:
        alice_balance = f'Error: {str(err)}'

    # TODO: send burn_events

    template = loader.get_template('alice.html')
    context = {'alice_balance': alice_balance}
    return HttpResponse(template.render(context, request))


# @login_required(login_url='/admin/')
def bob(request):
    # user = User.objects.get(username='bob')
    # if user != request.user:
    #     return JsonResponse({'error': 'user is not "bob". only bob can visit this page.'}, status=403)

    bob_address = Config.objects.get().bob_bsc_address
    if not bob_address:
        return JsonResponse({'error': 'Bob\'s BSC address is not specified in admin/'})

    try:
        cf = ContractFunctions(is_bsc=True)
        bob_balance = cf.balance_of(bob_address)
    except Exception as err:
        bob_balance = f'Error: {str(err)}'

    # TODO: send mint_events

    template = loader.get_template('bob.html')
    context = {'bob_balance': bob_balance}
    return HttpResponse(template.render(context, request))


def compile_contract(request):
    if request.method == 'POST':
        if compile_the_contract():
            config = Config.objects.get()
            config.is_contract_compiled = True
            config.save()
            return redirect('admin-panel')


def deploy_eth(request):
    if request.method == 'POST':
        deployed, address = deploy_eth_contract()
        if deployed:
            config = Config.objects.get()
            config.is_eth_deployed = True
            config.deployed_eth_contract_address = address
            config.save()
            return redirect('admin-panel')


def deploy_bsc(request):
    if request.method == 'POST':
        deployed, address = deploy_bsc_contract()
        if deployed:
            config = Config.objects.get()
            config.is_bsc_deployed = True
            config.deployed_bsc_contract_address = address
            config.save()
            return redirect('admin-panel')


def init_eth(request):
    if request.method == 'POST':
        data = request.POST
        eth_init_value = int(data.get('eth_init_value'))
        if eth_init_value:
            cf = ContractFunctions(is_bsc=False)
            res = cf.initial(eth_init_value)
            return redirect('admin-panel')


def init_bsc(request):
    if request.method == 'POST':
        data = request.POST
        bsc_init_value = int(data.get('bsc_init_value'))
        if bsc_init_value:
            cf = ContractFunctions(is_bsc=True)
            res = cf.initial(bsc_init_value)
            return redirect('admin-panel')


def transfer_eth(request):
    if request.method == 'POST':
        data = request.POST
        eth_transfer_address = data.get('eth_transfer_address')
        eth_transfer_value = data.get('eth_transfer_value')
        if all([eth_transfer_address, eth_transfer_value]):
            cf = ContractFunctions(is_bsc=False)
            res = cf.transfer(eth_transfer_address, int(eth_transfer_value))
            return redirect('admin-panel')
        else:
            return JsonResponse({"Error": "Bad address/value."})


def transfer_bsc(request):
    if request.method == 'POST':
        data = request.POST
        bsc_transfer_address = data.get('bsc_transfer_address')
        bsc_transfer_value = data.get('bsc_transfer_value')
        if all([bsc_transfer_address, bsc_transfer_value]):
            cf = ContractFunctions(is_bsc=True)
            res = cf.transfer(bsc_transfer_address, int(bsc_transfer_value))
            return redirect('admin-panel')
        else:
            return JsonResponse({"Error": "Bad address/value."})


def alice_burn(request):
    form_data = request.POST
    # TODO burn_value, burn_bob_bsc_account, burn_bsc_contract
    return JsonResponse({})
