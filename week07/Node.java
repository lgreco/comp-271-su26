class Node {

    private String payload;
    private Node next;
    private Node prev;

    public Node(String payload) {
        this.payload = payload;
        this.next = null;
        this.prev = null;
    }

    public static void main(String[] args) {
        Node test1 = new Node("Chicago");
        Node test2 = new Node(2026);
    }

}
