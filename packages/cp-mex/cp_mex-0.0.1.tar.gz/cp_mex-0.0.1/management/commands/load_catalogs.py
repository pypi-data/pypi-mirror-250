from django.core.management.base import BaseCommand
from ...models import *
from django.conf import settings
import csv

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("[!] Loading MX addresses...")
        self.load_states()
        self.load_zipcodes()
        self.load_delegations()
        self.load_suburbs()
    
    def load_states(self):
        with open(f"{settings.BASE_DIR}/catalogo_cp_mex/catalogs/states.csv") as csv_file:
            states_to_create = []
            csv_reader = csv.reader(csv_file)

            for row in csv_reader:
                pk = row[0]
                state_name = row[1].title()
                state_id = row[2]

                state = State(id=pk, name=state_name, state_id=state_id)
                states_to_create.append(state)

            State.objects.bulk_create(states_to_create)


    def load_zipcodes(self):
        with open(f"{settings.BASE_DIR}/catalogo_cp_mex/catalogs/zipcodes.csv") as csv_file:
            zipcodes_to_create = []
            csv_reader = csv.reader(csv_file)

            for row in csv_reader:
                pk = row[0]
                zip_code = row[1]

                zipcode = Zipcode(id=pk, zipcode=zip_code)
                zipcodes_to_create.append(zipcode)

            Zipcode.objects.bulk_create(zipcodes_to_create)


    def load_delegations(self):
        state_dict = {state.pk: state for state in State.objects.all()}

        with open(f"{settings.BASE_DIR}/catalogo_cp_mex/catalogs/delegations.csv") as csv_file:
            delegations_to_create = []
            csv_reader = csv.reader(csv_file)

            for row in csv_reader:
                pk = row[0]
                delegation_name = row[1]
                delegation_id = row[2]
                state_id = row[3]

                state = state_dict.get(int(state_id))

                delegation = Delegation(
                    id=pk,
                    name=delegation_name,
                    delegation_id=delegation_id,
                    state=state,
                )
                delegations_to_create.append(delegation)

            Delegation.objects.bulk_create(delegations_to_create)


    def load_suburbs(self):
        delegation_dict = {
            delegation.pk: delegation for delegation in Delegation.objects.all()
        }
        state_dict = {state.pk: state for state in State.objects.all()}
        zipcode_dict = {zipcode.pk: zipcode for zipcode in Zipcode.objects.all()}

        with open(f"{settings.BASE_DIR}/catalogo_cp_mex/catalogs/suburbs.csv") as csv_file:
            suburbs_to_create = []
            csv_reader = csv.reader(csv_file)

            for row in csv_reader:
                suburb_name = row[1]
                suburb_id = row[2]
                delegation_id = row[3]
                state_id = row[4]
                zipcode_id = row[5]

                state = state_dict.get(int(state_id))
                delegation = delegation_dict.get(int(delegation_id))
                zipcode = zipcode_dict.get(int(zipcode_id))

                suburb = Suburb(
                    name=suburb_name,
                    suburb_id=suburb_id,
                    zipcode=zipcode,
                    state=state,
                    delegation=delegation,
                )
                suburbs_to_create.append(suburb)

            Suburb.objects.bulk_create(suburbs_to_create)