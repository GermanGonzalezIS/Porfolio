package mx.edu.uaz.ingsoftware.poo2.clientemateriasde38192814;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonParseException;
import com.google.gson.reflect.TypeToken;

import java.io.IOException;
import java.lang.reflect.Type;
import java.net.MalformedURLException;
import java.util.ArrayList;
import java.util.List;


import mx.edu.uaz.ingsoftware.poo2.clientemateriasde38192814.entidades.Materia;
import mx.edu.uaz.ingsoftware.poo2.clientemateriasde38192814.utils.HttpUtils;

public class MainActivity extends AppCompatActivity {

    private ListView listaMaterias;
    private List<Materia> datos;
    private ArrayAdapter<Materia> adapterMateria;
    public static final int SOLICITUD_NUEVA=101;
    public static final int SOLICITUD_EXISTENTE=102;
    public static final int SOLICITUD_AGREGADA=103;
    public static final int MATERIA_ELIMINADA=104;
    public static final int MATERIA_MODIFICADA=105;
    public static final int STATUS_OK=0;
    public static final int STATUS_ERROR_FORMATO=1;
    public static final int STATUS_ERROR_ES=2;
    public static final int STATUS_ERROR_URL=3;

    /**
     * Constructor de la clase que maneja todos los eventos del MainActivity
     * hace referencia a los objetos de la interfaz de usuario
     * @param savedInstanceState
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        listaMaterias = findViewById(R.id.ListView_Materias);
        Button btnInferior= new Button(this);
        btnInferior.setText(R.string.texto_boton_nueva);
        manejadorlistaMaterias man = new manejadorlistaMaterias();
        btnInferior.setOnClickListener(man);
        listaMaterias.addFooterView(btnInferior);
        listaMaterias.setOnItemClickListener(man);
        if(savedInstanceState==null){
            cargaDatos();
        }

    }

    /**
     * Clae interna manejadorlistaMaterias se encarga de manejar los eventos de la listaMaterias
     * diferiencia si se dio click en una materia nueva o una ya existente
     */
    private class manejadorlistaMaterias implements AdapterView.OnItemClickListener, View.OnClickListener {
        @Override
        /**
         * materia nueva
         */
        public void onClick(View v) {
            Intent intent = new Intent(MainActivity.this, Activity_Detalle_Materia.class);
            startActivityForResult(intent, SOLICITUD_NUEVA);
        }

        /**
         * Materia ya existente
         * @param parent
         * @param view
         * @param position
         * @param id
         */
        @Override
        public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
            Materia m = (Materia) parent.getItemAtPosition(position);
            Intent intent = new Intent(MainActivity.this, Activity_Detalle_Materia.class);
            intent.putExtra("info", m);
            startActivityForResult(intent, SOLICITUD_EXISTENTE);
        }
    }

    /**
     * Metodo encargado de llamar a la clase que se encarga de extraer los datos enviados por la
     * clase HttpUtils
     */
    private void cargaDatos(){
        CargadorListaMaterias carga = new CargadorListaMaterias();
        String urlBase = getString(R.string.url_base)+"materia";
        carga.execute(urlBase);
    }

    /**
     * Clase que se llama en el metodo anterior, es una tarea asincrona se encarga de interpretar la respuesta de la
     * clase HttpUtils y de llenar la lista Materias
     */
    private class CargadorListaMaterias extends AsyncTask<String,Void,List<Materia>> {
        private int status;
        @Override
        /**
         * Metodo que se realiza despues de la ejecucion
         */
        protected void onPostExecute(List<Materia> materias) {
            super.onPostExecute(materias);
            if (status==STATUS_OK){
                adapterMateria = new ArrayAdapter<Materia>(MainActivity.this,android.R.layout.simple_list_item_1,materias);
                listaMaterias.setAdapter(adapterMateria);
            }
            else if (status==STATUS_ERROR_FORMATO){
                muestraToast(R.string.texto_error_formato);
            }
            else if (status==STATUS_ERROR_ES){
                muestraToast(R.string.texto_error_es);
            }
            else if (status==STATUS_ERROR_URL){
                muestraToast(R.string.texto_error_url);
            }
        }

        /**
         * Metodo de ejecucion realiza la interpretacion de la respuesta de HttpUtils
         * @param strings
         * @return
         */
        @Override
        protected List<Materia> doInBackground(String... strings) {
            List<Materia> info = new ArrayList<>();
            status = STATUS_OK;
            try{
                String respuesta= HttpUtils.httpGet(strings[0],"application/json");
                Type tipoListaMateria = new TypeToken<List<Materia>>() {}.getType();
                GsonBuilder constructor = new GsonBuilder();
                Gson gson = constructor.create();
                info=gson.fromJson(respuesta,tipoListaMateria);
            }catch (MalformedURLException eurl){
                status=STATUS_ERROR_URL;
                eurl.getStackTrace();
            }
            catch (IOException eio){
                status = STATUS_ERROR_ES;
                eio.printStackTrace();
            }
            catch (JsonParseException ejson){
                status=STATUS_ERROR_FORMATO;
                ejson.printStackTrace();
            }
            return info;
        }
    }

    /**
     * clase que se encarga de mostrar un toast
     * @param id
     */
    private void muestraToast(int id){
        Toast.makeText(this, id,Toast.LENGTH_LONG).show();
    }

    /**
     * Clase que se encarga de analizar la respuesta enviada del Activity_Detalle_Materia
     * Se ancarga de hacer los cambios correspondientes segun la instruccion ejecutada
     * @param requestCode
     * @param resultCode
     * @param data
     */
    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == SOLICITUD_NUEVA){
            if (resultCode==RESULT_OK){
                Materia nueva =(Materia) data.getSerializableExtra("info");
                adapterMateria.add(nueva);
            }
        }
        else {
            if (resultCode==RESULT_OK){
                Materia cambios = (Materia) data.getSerializableExtra("info");
                int op = data.getIntExtra("operacion",0);
                adapterMateria.remove(cambios);
                if(op == MATERIA_MODIFICADA){
                    adapterMateria.add(cambios);
                }
            }
        }
    }

}
