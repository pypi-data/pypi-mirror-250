import json
import logging
from . import schemas
from odoo.http import Response
from odoo.tools.translate import _
from odoo.addons.component.core import Component
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CsInvoiceService(Component):
    _inherit = "base.rest.private_abstract_service"
    _name = "cs.invoice.service"
    _usage = "cs-invoice"
    _description = """
        Invoice Services
    """

    def create(self, **params):
        _logger.info(str(self.work.request.httprequest.headers))
        reference_invoice = self._filter_reference(params.get('reference', ""))
        is_exist_invoice_by_ref = self.env['account.invoice'].search([("name", "=", reference_invoice)])
        if is_exist_invoice_by_ref:
            raise ValidationError(
                f"The invoice reference is duplicate ref:{reference_invoice}")
        create_dict = self._prepare_create(params)
        invoice = self.env['account.invoice'].create(create_dict)
        invoice.message_post(
            subject="Cs prepayment invoice created from APP",
            body=str(params),
            message_type="notification"
        )
        return Response(
            json.dumps({
                'message': _("Creation ok"),
                'id': str(invoice.id),
            }),
            status=200,
            content_type="application/json"
        )

    def _validator_create(self):
        return schemas.S_CS_INVOICE_CREATE

    def _prepare_create(self, params):
        company = self.env.user.company_id
        reference_invoice = self._filter_reference(params.get('reference', ""))
        customer = params.get('customer', False)
        if not customer:
            raise ValidationError(_("Customer details must be provided."))

        cs_person_index = self._filter_reference(customer.get('reference', ''))
        related_partners = self.env['res.partner'].search([('cs_person_index', '=', cs_person_index)])

        if not related_partners:
            customer_email = customer.get('email')
            related_partners = self.env['res.partner'].search([('email', '=', customer_email)])
            if not related_partners:
                raise ValidationError(f"No partner found with email: {customer_email}")

            related_partners[0].write({'cs_person_index': cs_person_index})

        if len(related_partners) != 1:
            raise ValidationError(f"Partner identification error with reference: {cs_person_index}")

        create_dict = {
            'state': 'draft',
            'type': 'out_invoice',
            'name': reference_invoice,
            'journal_id': company.cs_app_oneshot_account_journal_id.id,
            'invoice_email_sent': False,
            'invoice_template': 'cs_app_invoice',
            'payment_mode_id': company.cs_app_oneshot_payment_mode_id.id,
            'partner_id': related_partners[0].id,
            'date_invoice': params.get('date'),
        }

        items = params.get('items', False)
        if items:
            lines_list = []
            for item in items:
                quantity, price = self._process_price_quantity(item['quantity'], item['price'])
                taxes_l = [(4, tax.id) for tax in company.cs_app_oneshot_product_id.taxes_id]
                lines_list.append((0, 0, {
                    'product_id': company.cs_app_oneshot_product_id.id,
                    'name': item['description'],
                    'price_unit': price,
                    'quantity': quantity,
                    'account_id': company.cs_app_oneshot_product_id.property_account_income_id.id,
                    'account_analytic_id': company.cs_app_oneshot_product_id.income_analytic_account_id.id,
                    'line_type': 'default',
                    'invoice_line_tax_ids': taxes_l,
                }))
            create_dict['invoice_line_ids'] = lines_list

        return create_dict

    @staticmethod
    def _filter_reference(reference):
        return reference.replace("T/", '').split('/', maxsplit=1)[0]

    @staticmethod
    def _process_price_quantity(quantity, price):
        """
        If the price is 1 cent and the quantities are greater than 50, multiply cents by the quantity
        return: tuple(quantity, price)
        """
        if quantity > 50 and price == 0.01:
            return 1, (quantity * price)
        return quantity, price
