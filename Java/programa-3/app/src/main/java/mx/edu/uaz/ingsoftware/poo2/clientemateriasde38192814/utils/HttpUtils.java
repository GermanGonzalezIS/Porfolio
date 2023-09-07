package mx.edu.uaz.ingsoftware.poo2.clientemateriasde38192814.utils;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Clase encargada de hacer la solicitud al servicio rest segun la operacion que se desea realizar
 */
public class HttpUtils {

    public static String httpGet(String url, String acceptType) throws IOException {
        URL urlservicio;
        HttpURLConnection conn = null;
        InputStream is;
        String respuesta = null;

        urlservicio = new URL(url);
        conn = (HttpURLConnection) urlservicio.openConnection();
        if (acceptType != null)
            conn.setRequestProperty("Accept", acceptType);
        int codigo = conn.getResponseCode();
        if (codigo == HttpURLConnection.HTTP_OK) {
            is = conn.getInputStream();
            BufferedReader entrada = new BufferedReader(new InputStreamReader(is));
            respuesta = entrada.readLine();
        }
        return respuesta;
    }

    public static String httpPostPutDelete(String url, String datos, String contentType, String method)
            throws IOException {
        URL urlservicio;
        HttpURLConnection conn = null;
        OutputStream os;
        InputStream is;
        String respuesta = "false";

        urlservicio = new URL(url);
        conn = (HttpURLConnection) urlservicio.openConnection();
        conn.setRequestMethod(method);
        if (!method.equals("DELETE")) {
            conn.setDoOutput(true);
            byte info[] = datos.getBytes();
            if (contentType != null) {
                conn.setRequestProperty("Content-Type", contentType);
            }
            conn.setRequestProperty("Content-Length" ,
                    Integer.toString(info.length));
            os = conn.getOutputStream();
            os.write(info);
        }

        int codigo = conn.getResponseCode();
        if (codigo == 204) {
            respuesta = "true";
        }
        else if (codigo==200) {
            is = conn.getInputStream();
            BufferedReader entrada = new BufferedReader(new InputStreamReader(is));
            respuesta = entrada.readLine();
        }
        return respuesta;
    }


}

