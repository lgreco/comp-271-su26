class Node<T> {

    private T payload;
    private Node next;
    private Node prev;

    public Node(T payload) {
        this.payload = payload;
        this.next = null;
        this.prev = null;
    }

    public static void main(String[] args) {
        Node<String> test1 = new Node("Chicago");
        Node<Int> test2 = new Node(2026);
    }

}
