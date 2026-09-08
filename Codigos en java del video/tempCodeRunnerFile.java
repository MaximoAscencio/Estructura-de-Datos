import java.util.ArrayList;

public class Dinamica { 
    public static void main(String[] args) {
        
        ArrayList<String> frutas = new ArrayList<>();
        
        frutas.add("mango"); 
        frutas.add("manzana");
        frutas.add("banana"); 
        frutas.add("uvas"); 
        System.out.println(frutas); 
        frutas.remove(0);
        frutas.remove(1); 
        frutas.add("sandía"); 
        System.out.println(frutas); 
    }
}