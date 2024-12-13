package adf_core_python.gateway;

import rescuecore2.registry.Registry;
import rescuecore2.standard.entities.StandardEntityFactory;
import rescuecore2.standard.entities.StandardPropertyFactory;
import rescuecore2.standard.messages.StandardMessageFactory;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class Gateway extends Thread {
    private final int port;
    private final ArrayList<Coordinator> coordinators;
    private boolean running = true;

    public Gateway(int port) {
        this.port = port;
        this.coordinators = new ArrayList<>();

        Registry.SYSTEM_REGISTRY.registerFactory(StandardEntityFactory.INSTANCE);
        Registry.SYSTEM_REGISTRY.registerFactory(StandardMessageFactory.INSTANCE);
        Registry.SYSTEM_REGISTRY.registerFactory(StandardPropertyFactory.INSTANCE);
    }

    @Override
    public void run() {
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            serverSocket.setReuseAddress(true);
            while (running) {
                Socket socket = serverSocket.accept();
                Coordinator coordinator = new Coordinator(socket);
                coordinator.start();
                coordinators.add(coordinator);
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public void shutdown() {
        running = false;
        for (Coordinator coordinator : coordinators) {
            coordinator.shutdown();
        }
    }
}
