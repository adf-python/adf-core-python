package adf_core_python;

import adf_core_python.core.gateway.Gateway;

public class Main {
    public static void main(String[] args) {
        Gateway gateway = new Gateway(27941);
        gateway.start();
    }
}
