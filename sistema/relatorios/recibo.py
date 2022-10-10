from sistema.relatorios.base import Pdf
from sistema.models import Venda, ItemVenda
from django.db.models.query import QuerySet


class Recibo(Pdf):

    def __init__(self, modelo: str, venda: Venda, items: QuerySet[ItemVenda]) -> None:
        super().__init__(modelo)

        self.model = venda
        self.items = items

    def gerar(self) -> None:
        self.nr_nota()
        self.cliente()
        self.data()
        self.items_venda()
        self.total()

    def items_venda(self) -> None:
        y = 680
        self.can.setFontSize(size=8)
        for index, item in enumerate(self.items):
            self.can.drawString(65, y, f'{index+1}')
            self.can.drawString(100, y, f'{item.produto}')

            self.can.drawString(65, y - 380, f'{index + 1}')
            self.can.drawString(100, y - 380, f'{item.produto}')

            self.can.setFontSize(size=7)
            self.can.drawString(330, y, f'{item.unidade}')
            self.can.drawString(375, y, f'{item.get_valor}')
            self.can.drawString(435, y, f'{item.quantidade}')
            self.can.drawString(490, y, f'{item.get_total}')

            self.can.drawString(330, y-380, f'{item.unidade}')
            self.can.drawString(375, y-380, f'{item.get_valor}')
            self.can.drawString(435, y-380, f'{item.quantidade}')
            self.can.drawString(490, y-380, f'{item.get_total}')

            y -= 10

    def total(self) -> None:
        y = 500
        self.can.setFontSize(size=10)
        self.can.drawString(60, y, f'Total:')
        self.can.drawString(480, y, f'{self.model.get_total}')

        self.can.drawString(60, y-380, f'Total:')
        self.can.drawString(480, y-380, f'{self.model.get_total}')

    def data(self) -> None:
        self.can.setFontSize(size=8)
        self.can.drawString(440, 732, f'{self.model.get_data}')
        self.can.drawString(440, 352, f'{self.model.get_data}')

    def cliente(self) -> None:
        self.can.setFontSize(size=8)
        self.can.drawString(100, 732, f'{self.model.cliente}')
        self.can.drawString(100, 352, f'{self.model.cliente}')

    def nr_nota(self) -> None:
        self.can.setFontSize(size=12)
        self.can.drawString(380, 780, f'NOTA DE ENTREGA Nº {self.model}')
        self.can.drawString(380, 400, f'NOTA DE ENTREGA Nº {self.model}')

    def salvar(self) -> None:
        self.can.save()
