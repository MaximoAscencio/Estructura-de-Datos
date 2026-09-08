import javax.swing.JOptionPane;
public class MemoriaEstatica {
    public static void main(String[] args) {
        // Se declara la variable "calificaciones" y se reservan exactamente 5 espacios enteros [1]
        int[] calificaciones = new int[5]; 
        
        // Un ciclo 'for' que se repite 5 veces (desde 0 hasta 4) [2]
        for (int i = 0; i < 5; i++) {
            calificaciones [i] = Integer.parseInt(JOptionPane.showInputDialog(null,"captura la" +  " calificación:" ));
        }
    }
}