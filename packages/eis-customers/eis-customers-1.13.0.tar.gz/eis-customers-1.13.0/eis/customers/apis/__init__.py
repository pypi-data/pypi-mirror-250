
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from eis.customers.api.authentication_api import AuthenticationApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from eis.customers.api.authentication_api import AuthenticationApi
from eis.customers.api.claims_api import ClaimsApi
from eis.customers.api.customers_api import CustomersApi
from eis.customers.api.documents_api import DocumentsApi
from eis.customers.api.invites_api import InvitesApi
from eis.customers.api.invoices_api import InvoicesApi
from eis.customers.api.leads_api import LeadsApi
from eis.customers.api.payments_api import PaymentsApi
from eis.customers.api.policies_api import PoliciesApi
from eis.customers.api.products_api import ProductsApi
from eis.customers.api.default_api import DefaultApi
