import java.rmi.Remote;
import java.rmi.RemoteException;

public interface MyServer extends Remote {
    String sayHello() throws RemoteException;
}
