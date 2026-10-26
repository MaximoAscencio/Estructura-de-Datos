
from abc import ABC, abstractmethod


# CLASE ORDER (PEDIDO)
class Order:
    def __init__(self, qtty, customer):
        self.customer = customer
        self.qtty = qtty

    def print(self):
        print("    Cliente: " + self.getCustomer())
        print("    Cantidad: " + str(self.getQtty()))
        print("    ------------")

    def getQtty(self):
        return self.qtty

    def getCustomer(self):
        return self.customer


# CLASE NODE (NODO)
class Node:
    def __init__(self, info):
        self.info = info
        self.next = None


# INTERFAZ QUEUE (COLA)
class QueueInterface(ABC):

    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def isEmpty(self):
        pass

    @abstractmethod
    def front(self):
        pass

    @abstractmethod
    def enqueue(self, info):
        pass

    @abstractmethod
    def dequeue(self):
        pass


# CLASE QUEUE (COLA ENLAZADA)
class Queue(QueueInterface):

    def __init__(self):
        self.top = None
        self.tail = None
        self.numElements = 0

    # Devuelve la cantidad de elementos en la cola
    def size(self):
        return self.numElements

    # Comprueba si la cola esta vacia
    def isEmpty(self):
        return self.numElements == 0

    # Consulta el primer pedido sin eliminarlo
    def front(self):
        if self.isEmpty():
            return None

        return self.top.info

    # Agrega un pedido al final de la cola
    def enqueue(self, info):
        newNode = Node(info)

        if self.isEmpty():
            self.top = newNode
        else:
            self.tail.next = newNode

        self.tail = newNode
        self.numElements += 1

    # Elimina y devuelve el primer pedido
    def dequeue(self):
        if self.isEmpty():
            return None

        info = self.top.info
        self.top = self.top.next
        self.numElements -= 1

        if self.top is None:
            self.tail = None

        return info

    # Muestra los pedidos y el tamaño de la cola
    def printInfo(self):
        print("********* ESTADO DE LA COLA *********")
        print("    Tamaño: " + str(self.size()))

        node = self.top
        element = 1

        while node is not None:
            print("    ** Elemento " + str(element))
            node.info.print()

            node = node.next
            element += 1

        print("************************************\n")

    # Obtiene el pedido de una posicion sin eliminarlo
    def getNth(self, pos):
        if pos < 1 or pos > self.size():
            return None

        node = self.top

        for _ in range(1, pos):
            node = node.next

        return node.info


# CLASE TESTQUEUE (PRUEBAS DE LA COLA)
class TestQueue:

    @staticmethod
    def main():
        queue = Queue()

        # Insertar primer pedido
        queue.enqueue(Order(20, "cust1"))
        queue.printInfo()

        # Insertar segundo pedido
        queue.enqueue(Order(30, "cust2"))
        queue.printInfo()

        # Insertar tercer pedido
        queue.enqueue(Order(40, "cust3"))
        queue.printInfo()

        # Insertar cuarto pedido
        queue.enqueue(Order(50, "cust3"))
        queue.printInfo()

        # Consultar el primer pedido sin eliminarlo
        print("Primer pedido (front):")
        first = queue.front()

        if first is not None:
            first.print()

        # Obtener el tercer pedido sin eliminarlo
        print("\nTercer pedido (getNth(3)):")
        third = queue.getNth(3)

        if third is not None:
            third.print()

        # Comprobar una posicion fuera de rango
        print("\nPosición 5:", queue.getNth(5))
        print()

        # Extraer el primer pedido
        print("Extrayendo el primer pedido:")
        queue.dequeue()
        queue.printInfo()

        # Extraer el siguiente pedido
        print("Extrayendo el siguiente pedido:")
        queue.dequeue()
        queue.printInfo()


if __name__ == "__main__":
    TestQueue.main()
