package mx.edu.uaz.ingsoftware.poo2.clientemateriasde38192814;

import androidx.appcompat.app.AppCompatActivity;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
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
import java.util.concurrent.ExecutionException;

import mx.edu.uaz.ingsoftware.poo2.clientemateriasde38192814.entidades.Carrera;
import mx.edu.uaz.ingsoftware.poo2.clientemateriasde38192814.entidades.Materia;
import mx.edu.uaz.ingsoftware.poo2.clientemateriasde38192814.utils.HttpUtils;

public class Activity_Detalle_Materia extends AppCompatActivity {
    private ArrayAdapter<Carrera> datosSpiner;
    private ArrayAdapter<Carrera> adapterCarrera;
    private Spinner spinerCarrera;
    private EditText editClave;
    private EditText editNombre;
    private EditText editSemestre;
    private Button btnEliminar;
    private Button btnGuardar;
    private boolean esNueva;
    private Materia m;
    private AlertDialog dialogoConfirmacionEliminar;

    /**
     * Constructor de la clase que maneja los evetos del activity_detalle_materia
     * hace referencia a todos los objetos de la interfaz del usuario
     * @param savedInstanceState
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity__detalle__materia);
        editClave=findViewById(R.id.edit_Clave_Materia);
        editNombre=findViewById(R.id.edit_Nombre_Materia);
        editSemestre=findViewById(R.id.edit_Semestre_Materia);
        btnEliminar=findViewById(R.id.button_Eliminar);
        btnGuardar =findViewById(R.id.button_Agregar);
        spinerCarrera=findViewById(R.id.spinner_Carrera);
        obtenInfo();
        creaDialogoConfirmacion();
    }

    /**
     * Metodo que se encarga de extraer la informacion extra del Intent enviado
     * si es diferente de null se llenan los editText con informacion de la materia obtenida
     */
    private void obtenInfo(){
        try {
            cargaDatos();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        Carrera cVacia=new Carrera();
        datosSpiner.add(cVacia);
        spinerCarrera.setAdapter(datosSpiner);
        Intent intent = getIntent();
        m = (Materia) intent.getSerializableExtra("info");
        if (m==null){
            esNueva=true;
            btnEliminar.setVisibility(View.GONE);
            spinerCarrera.setSelection(datosSpiner.getCount()-1);
        }
        else{
            esNueva=false;
            editClave.setText(m.getClaveMateria());
            editNombre.setText(m.getNombreMateria());
            editSemestre.setText(String.valueOf(m.getSemestre()));
            for(int i=0;i<datosSpiner.getCount();i++){
                if(m.getClaveCarrera().equals(datosSpiner.getItem(i).getClaveCarrera())){
                    spinerCarrera.setSelection(i);
                }
            }
            editClave.setEnabled(false);
            btnGuardar.setText(R.string.texto_boton_guardar);
        }
    }

    /**
     * Metodo que llama a una clase encargada de interpretar la respuesta de la clase HttpUtils para llenar el
     * spinner con las carreras obtenidas de la base de datos
     * @throws ExecutionException
     * @throws InterruptedException
     */
    private void cargaDatos() throws ExecutionException, InterruptedException {
        CargadorSpinnerCarreras carga = new CargadorSpinnerCarreras();
        String urlBase = getString(R.string.url_base)+"carrera";
        carga.execute(urlBase);
        datosSpiner = new ArrayAdapter<Carrera>(Activity_Detalle_Materia.this,android.R.layout.simple_spinner_item,carga.get());
    }

    private void muestraToast(int id){
        Toast.makeText(this, id,Toast.LENGTH_LONG).show();
    }

    /**
     * Clase que se manda llamar en el metodo cargaDatos, interpreta la respuesta del HttpUtils
     */
    private class CargadorSpinnerCarreras extends AsyncTask<String,Void,List<Carrera>> {
        private int status;

        /**
         * Metodo que realiza las acciones correspondientes despues de la ejecucion
         * @param carreras
         */
        @Override
        protected void onPostExecute(List<Carrera> carreras) {
            super.onPostExecute(carreras);

            if (status==MainActivity.STATUS_OK){
                adapterCarrera = new ArrayAdapter<Carrera>(Activity_Detalle_Materia.this,android.R.layout.simple_spinner_item,carreras);
            }
            else if (status==MainActivity.STATUS_ERROR_FORMATO){
                muestraToast(R.string.texto_error_formato);
            }
            else if (status==MainActivity.STATUS_ERROR_ES){
                muestraToast(R.string.texto_error_es);
            }
            else if (status==MainActivity.STATUS_ERROR_URL){
                muestraToast(R.string.texto_error_url);
            }
        }

        /**
         * Metodo que se ejecuta realiza la interpretacion de la respuesta dada por la clase HttpUtils
         * @param strings
         * @return
         */
        @Override
        protected List<Carrera> doInBackground(String... strings) {
            List<Carrera> info = new ArrayList<>();
            status = MainActivity.STATUS_OK;
            try{
                String respuesta= HttpUtils.httpGet(strings[0],"application/json");
                Type tipoListaCarrera=new TypeToken<List<Carrera>>() {}.getType();
                GsonBuilder constructor = new GsonBuilder();
                Gson gson = constructor.create();
                info=gson.fromJson(respuesta,tipoListaCarrera);
            }catch (MalformedURLException eurl){
                status=MainActivity.STATUS_ERROR_URL;
                eurl.getStackTrace();
            }
            catch (IOException eio){
                status = MainActivity.STATUS_ERROR_ES;
                eio.printStackTrace();
            }
            catch (JsonParseException ejson){
                status=MainActivity.STATUS_ERROR_FORMATO;
                ejson.printStackTrace();
            }
            return info;
        }
    }

    /**
     * Metodo que termina este activity
     * @param v
     */
    public void regresar(View v){
        finish();
    }
    /**
     * Metodo para crear un cuadro de dialogo de confirmacion de eliminacion
     */
    private void creaDialogoConfirmacion() {
        // Se crea un constructor de cuadros de dialogo
        AlertDialog.Builder constructor = new AlertDialog.Builder(this);
        // Se establece el titulo del cuadro de dialogo
        constructor.setTitle(R.string.titulo_confirmacion_eliminar);
        // Se estable el mensaje del cuadro de dialogo
        constructor.setMessage(R.string.texto_confirmacion_eliminar);
        // Se establece el texto del boton de aceptacion asi como el manejador
        constructor.setPositiveButton(R.string.titulo_opcion_si, new ManejadorConfirmacion());
        // Se establece el texto del boton de cancelacio  asi como el manejador
        constructor.setNegativeButton(R.string.titulo_opcion_no, null);
        // Se crea el cuadro de dialogo
        dialogoConfirmacionEliminar = constructor.create();
    }

    /**
     * Metodo que maneja la confirmacion para eliminar una materia, si es no no realiza nada, si la respuesta es si manda llamar la clase
     * HiloModificadorMateria y lo ejecuta con la url Correspondiente al servicio Rest
     */
    private class ManejadorConfirmacion implements DialogInterface.OnClickListener{
        @Override
        public void onClick(DialogInterface dialog, int which) {
            HiloModificadorMateria hilo= new HiloModificadorMateria(MainActivity.MATERIA_ELIMINADA);
            hilo.execute(getString(R.string.url_base)+"materia/"+m.getClaveMateria());
        }
    }

    /**
     * clase que se encarga de procesar el tipo de operacion que se desea realizar a travez de
     * la clase HttpUtils
     */
    private class HiloModificadorMateria extends AsyncTask<String, Void, String> {
        private int status;
        private int tipo;

        /**
         * Clase que se encarga de llamar al metodo muestraToast segun la operacion realizada
         * con el mensaje correspondiente
         * @param tipo
         */
        public HiloModificadorMateria(int tipo) {
            this.tipo = tipo;
        }

        @Override
        protected void onPostExecute(String s) {
            super.onPostExecute(s);
            if (status == MainActivity.STATUS_OK) {
                if (s.equals("true")) {
                    muestraToast((R.string.texto_exito));
                    regresarDatos(tipo);
                } else {
                    muestraToast(R.string.texto_error_operacion);
                }
            } else if (status == MainActivity.STATUS_ERROR_URL) {
                muestraToast(R.string.texto_error_url);
            } else {
                muestraToast(R.string.texto_error_es);
            }
        }

        /**
         * Metodo que se ejecuta define el tipo de metodo que se quiere realizar manda llamar a la
         * clase HttpUtils para realizar las opèraciones POST PUT y DELETE segun corresponda
         * @param strings
         * @return
         */
        @Override
        protected String doInBackground(String... strings) {
            String metodo=null;
            String datos=null;
            String tipoContenido=null;
            String respuesta = "false";
            status=MainActivity.STATUS_OK;
            if (tipo == MainActivity.SOLICITUD_AGREGADA){
                metodo= "POST";
            }
            else if (tipo == MainActivity.MATERIA_ELIMINADA){
                metodo= "DELETE";
            }
            else if (tipo == MainActivity.MATERIA_MODIFICADA){
                metodo= "PUT";
            }
            if (tipo == MainActivity.SOLICITUD_AGREGADA||tipo == MainActivity.MATERIA_MODIFICADA){
                Gson gson = new Gson();
                datos = gson.toJson(m);
                tipoContenido="application/json";
            }
            try{
                respuesta = HttpUtils.httpPostPutDelete(strings[0],datos,tipoContenido,metodo);
            }catch(MalformedURLException eurl){
                status= MainActivity.STATUS_ERROR_URL;
                eurl.printStackTrace();
            }catch(IOException eio){
                status= MainActivity.STATUS_ERROR_ES;
            }
            return respuesta;
        }
    }

    /**
     * Metodo que envia una respuesta al MainActivity de la operacion realizada
     * @param tipo
     */
    private void regresarDatos(int tipo){
        Intent intent = new Intent();
        intent.putExtra("info",m);
        intent.putExtra("operacion",tipo);
        setResult(RESULT_OK,intent);
        finish();
    }

    /**
     * Metodo que muestra un mensaje de confirmacion si se desea eliminar una materia
     * @param v
     */
    public void eliminaMateria(View v){
        dialogoConfirmacionEliminar.show();
    }

    /**
     * estrae los datos de los campos a llenar, verifica que no se encuentren vacios, si no se encuentran vacios manda llamar al hilo modificadr de materias para realizar
     * las operaciones con los datos de la materia
     * @param v
     */
    public void guardaMateria(View v){
        if(editClave.getText().toString().isEmpty()||editNombre.getText().toString().isEmpty()||editSemestre.toString().isEmpty()){
            muestraToast(R.string.texto_error_datos);
        }
        else{
            if (m==null){
                m=new Materia();
            }
            m.setClaveMateria(editClave.getText().toString());
            m.setNombreMateria(editNombre.getText().toString());
            m.setSemestre(Short.parseShort(editSemestre.getText().toString()));
            m.setClaveCarrera(datosSpiner.getItem(spinerCarrera.getSelectedItemPosition()).getClaveCarrera());
            HiloModificadorMateria hilo= null;
            if (esNueva){
                hilo = new HiloModificadorMateria(MainActivity.SOLICITUD_AGREGADA);
                hilo.execute(getString(R.string.url_base)+"materia");
            }
            else {
                hilo = new HiloModificadorMateria(MainActivity.MATERIA_MODIFICADA);
                hilo.execute(getString(R.string.url_base)+"materia/"+m.getClaveMateria());
            }
        }
    }

}
