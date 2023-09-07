package mx.edu.uaz.ingsoftware.poo2.clientemateriasde38192814.entidades;

import java.io.Serializable;


/**
 *
 * @author german_gonzalez
 */

public class Materia implements Serializable {

    private static final long serialVersionUID = 1L;

    private String claveMateria;


    private String nombreMateria;

    private short semestre;


    private String claveCarrera;

    public Materia() {
    }

    public Materia(String claveMateria) {
        this.claveMateria = claveMateria;
    }

    public Materia(String claveMateria, String nombreMateria, short semestre, String claveCarrera) {
        this.claveMateria = claveMateria;
        this.nombreMateria = nombreMateria;
        this.semestre = semestre;
        this.claveCarrera = claveCarrera;
    }

    public String getClaveMateria() {
        return claveMateria;
    }

    public void setClaveMateria(String claveMateria) {
        this.claveMateria = claveMateria;
    }

    public String getNombreMateria() {
        return nombreMateria;
    }

    public void setNombreMateria(String nombreMateria) {
        this.nombreMateria = nombreMateria;
    }

    public short getSemestre() {
        return semestre;
    }

    public void setSemestre(Short semestre) {
        this.semestre = semestre;
    }

    public String getClaveCarrera() {
        return claveCarrera;
    }

    public void setClaveCarrera(String claveCarrera) {
        this.claveCarrera = claveCarrera;
    }

    @Override
    public int hashCode() {
        int hash = 0;
        hash += (claveMateria != null ? claveMateria.hashCode() : 0);
        return hash;
    }

    @Override
    public boolean equals(Object object) {
        // TODO: Warning - this method won't work in the case the id fields are not set
        if (!(object instanceof Materia)) {
            return false;
        }
        Materia other = (Materia) object;
        if ((this.claveMateria == null && other.claveMateria != null) || (this.claveMateria != null && !this.claveMateria.equals(other.claveMateria))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return nombreMateria;
    }

}
