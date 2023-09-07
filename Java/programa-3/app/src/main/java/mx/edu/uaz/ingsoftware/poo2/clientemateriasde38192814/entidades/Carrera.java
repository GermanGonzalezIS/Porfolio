package mx.edu.uaz.ingsoftware.poo2.clientemateriasde38192814.entidades;

import java.io.Serializable;

public class Carrera implements Serializable {
    private static final long serialVersionUID = 1L;



    private String claveCarrera;


    private String nombreCarrera;

    public Carrera() {
    }

    public Carrera(String claveCarrera) {
        this.claveCarrera = claveCarrera;
    }

    public Carrera(String claveCarrera, String nombreCarrera) {
        this.claveCarrera = claveCarrera;
        this.nombreCarrera = nombreCarrera;
    }

    public String getClaveCarrera() {
        return claveCarrera;
    }

    public void setClaveCarrera(String claveCarrera) {
        this.claveCarrera = claveCarrera;
    }

    public String getNombreCarrera() {
        return nombreCarrera;
    }

    public void setNombreCarrera(String nombreCarrera) {
        this.nombreCarrera = nombreCarrera;
    }

    @Override
    public int hashCode() {
        int hash = 0;
        hash += (claveCarrera != null ? claveCarrera.hashCode() : 0);
        return hash;
    }

    @Override
    public boolean equals(Object object) {
        // TODO: Warning - this method won't work in the case the id fields are not set
        if (!(object instanceof Carrera)) {
            return false;
        }
        Carrera other = (Carrera) object;
        if ((this.claveCarrera == null && other.claveCarrera != null) || (this.claveCarrera != null && !this.claveCarrera.equals(other.claveCarrera))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return nombreCarrera;
    }

}

