import datetime
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template import loader

from core.models import Config, Event
from blockchain.compile_contract import compile_the_contract, is_contract_compiled
from blockchain.deploy import deploy_eth_contract, deploy_bsc_contract, contract_exists
from blockchain.functions import ContractFunctions


def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


# @login_required(login_url='/admin/')
def owner(request):
    # user = User.objects.get(username='admin')
    # if user != request.user:
    #     return JsonResponse({'error': 'user is not "admin". only admin can visit this page.'}, status=403)

    try:
        cf = ContractFunctions(is_bsc=False)
        eth_owner_balance = cf.balance_of(cf.owner_address)
    except Exception as err:
        eth_owner_balance = 'Error: Could not establish connection to ETH. ' + str(err)
    try:
        cf = ContractFunctions(is_bsc=True)
        bsc_owner_balance = cf.balance_of(cf.owner_address)
    except Exception as err:
        bsc_owner_balance = 'Error: Could not establish connection to BSC. ' + str(err)

    try:
        cf = ContractFunctions(is_bsc=False)
        eth_total_supply = cf.total_supply_amount()
    except Exception as err:
        eth_total_supply = 'Error: Could not establish connection to ETH. ' + str(err)
    try:
        cf = ContractFunctions(is_bsc=True)
        bsc_total_supply = cf.total_supply_amount()
    except Exception as err:
        bsc_total_supply = 'Error: Could not establish connection to BSC. ' + str(err)

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

    eth_owner = config.owner_eth_address
    bsc_owner = config.owner_bsc_address

    event_handler_status = config.event_handler_status

    template = loader.get_template('owner.html')
    context = {
        'is_compiled': is_compiled,
        'event_handler_status': event_handler_status,
        'is_eth_deployed': is_eth_deployed,
        'is_bsc_deployed': is_bsc_deployed,
        'eth_owner': eth_owner,
        'bsc_owner': bsc_owner,
        'eth_owner_balance': eth_owner_balance,
        'bsc_owner_balance': bsc_owner_balance,
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

    burn_events = Event.objects.filter(event_type=Event.EventType.BURNING).order_by('-created_at')

    template = loader.get_template('alice.html')
    context = {'alice_balance': alice_balance, 'burn_events': burn_events}
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

    mint_events = Event.objects.filter(event_type=Event.EventType.MINTING).order_by('-created_at')

    template = loader.get_template('bob.html')
    context = {'bob_balance': bob_balance, 'mint_events': mint_events}
    return HttpResponse(template.render(context, request))


def compile_contract(request):
    if request.method == 'POST':
        if compile_the_contract():
            config = Config.objects.get()
            config.is_contract_compiled = True
            config.save()
            return redirect('owner')


def deploy_eth(request):
    if request.method == 'POST':
        deployed, address = deploy_eth_contract()
        if deployed:
            config = Config.objects.get()
            config.is_eth_deployed = True
            config.deployed_eth_contract_address = address
            config.save()
            return redirect('owner')


def deploy_bsc(request):
    if request.method == 'POST':
        deployed, address = deploy_bsc_contract()
        if deployed:
            config = Config.objects.get()
            config.is_bsc_deployed = True
            config.deployed_bsc_contract_address = address
            config.save()
            return redirect('owner')


def init_eth(request):
    if request.method == 'POST':
        data = request.POST
        eth_init_value = int(data.get('eth_init_value'))
        if eth_init_value:
            cf = ContractFunctions(is_bsc=False)
            res = cf.initial(eth_init_value)
            return redirect('owner')


def init_bsc(request):
    if request.method == 'POST':
        data = request.POST
        bsc_init_value = int(data.get('bsc_init_value'))
        if bsc_init_value:
            cf = ContractFunctions(is_bsc=True)
            res = cf.initial(bsc_init_value)
            return redirect('owner')


def transfer_eth(request):
    if request.method == 'POST':
        data = request.POST
        eth_transfer_address = data.get('eth_transfer_address')
        eth_transfer_value = data.get('eth_transfer_value')
        if all([eth_transfer_address, eth_transfer_value]):
            cf = ContractFunctions(is_bsc=False)
            res = cf.transfer(eth_transfer_address, int(eth_transfer_value))
            res2 = cf.approve(eth_transfer_address, int(eth_transfer_value))
            return redirect('owner')
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
            return redirect('owner')
        else:
            return JsonResponse({"Error": "Bad address/value."})


def alice_burn(request):
    data = request.POST
    burn_value = data.get('burn_value')
    burn_bob_bsc_account = data.get('burn_bob_bsc_account')
    burn_bsc_contract = data.get('burn_bsc_contract')
    if not all([burn_value, burn_bob_bsc_account, burn_bsc_contract]):
        return JsonResponse({"Error": "Bad inputs."})

    cf_eth = ContractFunctions(is_bsc=False)
    cf_bsc = ContractFunctions(is_bsc=True)

    # check bsc contract:
    if burn_bsc_contract != cf_bsc.contract_address:
        return JsonResponse({"Error": f"Invalid BSC contract. {burn_bsc_contract} != {cf_bsc.contract_address}"})

    res = cf_eth.burn(outer_to_address=burn_bob_bsc_account, value=burn_value, contract=burn_bsc_contract)

    return redirect('alice')


def get_w3_and_contract_addresses(request):
    cf = Config.objects.get()
    eth_w3_url = cf.eth_url
    bsc_w3_url = cf.bsc_url
    eth_contract_address = cf.deployed_eth_contract_address
    bsc_contract_address = cf.deployed_bsc_contract_address
    return JsonResponse(
        {
            'eth_w3_url': eth_w3_url,
            'bsc_w3_url': bsc_w3_url,
            'eth_contract_address': eth_contract_address,
            'bsc_contract_address': bsc_contract_address,
        }, status=200)


def set_event_handler_status_true(request):
    cf = Config.objects.get()
    cf.event_handler_status = True
    cf.save()
    return JsonResponse({}, status=200)


def submit_event(request):
    if request.method == 'POST':
        data = request.POST
        event_type = data.get('event_type')
        payload = json.loads(data.get('payload'))
        created_at = datetime.datetime.now()
        if event_type == 'A':
            event_type = Event.EventType.APPROVAL
        elif event_type == 'T':
            event_type = Event.EventType.TRANSFER
        elif event_type == 'M':
            event_type = Event.EventType.MINTING
        elif event_type == 'B':
            event_type = Event.EventType.BURNING

        Event.objects.create(event_type=event_type, payload=payload, created_at=created_at)

        # minting:
        if event_type == Event.EventType.BURNING:
            cf = ContractFunctions(is_bsc=True)
            res = cf.mint(status=True, address_from=payload['_owner'], address_to=payload['_outerTo'],
                          value=payload['_value'], contract=cf.contract_address)
            if res:
                print('Mint successful')

        return JsonResponse({}, status=201)