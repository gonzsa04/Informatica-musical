using UnityEngine;
using System.Collections;

public class Fantasma : MonoBehaviour {
	
    RaycastHit hit;

	public float tiempo;

	void Avanza (){//responsable del movimiento del fantasma

       this.transform.Rotate(new Vector3(0, -90, 0));//gira a la izquierda
            while ((Physics.Raycast(this.transform.position, this.transform.forward, out hit,1f)))//mientras se choque con los muros o la salida
            {

                this.transform.Rotate(new Vector3(0, 90, 0));//gira a la izquierda y vuelve a mirar que tiene delante
            }
            this.transform.position += this.transform.forward;//una vez comprobado que no tiene nada delante sigue avanzando
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))//si colisiona con un objeto con tag player
            Debug.Log("Has muerto");
    }

    // Use this for initialization
    void Start () {
		InvokeRepeating ("Avanza", 0f, tiempo);//llama al metodo avanza cada x segundos(modificables desde el editor)
    }

}
