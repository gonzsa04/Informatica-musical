// ----------------------------------------------------------
// Material adicional de la práctica 3.
// Motores de Videojuegos - FDI - UCM
// ----------------------------------------------------------
// Profesor: Marco Antonio Gómez Martín
// ----------------------------------------------------------
using UnityEngine;
using System.Collections;

/// <summary>
/// Componente utilizado para hacer que la cámara se mueva
/// de forma que mantenga otro GO a la vista.
/// </summary>
/// El componente está pensado para ser añadido a una cámara
/// y configurado con el objeto al que enfocar (target)
/// 
/// En el arranque almacena la distancia y orientación relativa con ese
/// target y lo sigue por la escena cuando se mueve, manteniendo
/// fijas ambos valores.
/// 
/// El movimiento lo realiza de forma suave (el valor de suavizado
/// o lo que es lo mismo de velocidad a la que se adapta
/// a las posiciones del target) se puede configurar con el
/// editor (parámetro smoothLevel).
/// 
/// Además, hace esfuerzos por mantener el target a la vista. Si
/// se pone algo delante, le envía el mensaje "ActivaTransparencia",
/// con la esperanza de que se vuelva transparente.
public class SmoothCamera : MonoBehaviour {

    /// <summary>
    /// Objeto que se sigue (normalmente el jugador)
    /// </summary>
    public Transform target = null;

    /// <summary>
    /// Permite definir la cantidad de suavizado.
    /// Cuanto más grande, más rápido va. Con 0 no se mueve...
    /// </summary>
    public float smoothLevel = 1.0f;

    /// <summary>
    /// Distancia objetivo a mantener con el objetivo. Se utiliza
    /// directamente la que hay en el momento de arranque...
    /// </summary>
    private Vector3 offset = Vector3.zero;

    /// <summary>
    /// Magnitud de la distancia que se desea tener desde la
    /// cámara al target.
    /// </summary>
    private float offsetMag;

    /// <summary>
    /// Número de puntos que comprobamos
    /// </summary>
    private const int numCheckedPoints = 10;

    private Vector3 targetPosInTargetSpace;

    /// <summary>
    /// Registra el "offset" que hay que mantener entre la cámara y el
    /// jugador, en base a las posiciones iniciales de ambos.
    /// </summary>
    /// Usa Awake en lugar de Start para ejecutarse antes de los Start
    /// de target, etc., por si acaso éstos son colocados en otro sitio.
    void Awake()
    {

        if (target == null)
        {
            Debug.LogWarning("Smooth camera sin objeto asignado. Componente deshabilitado.");
            enabled = false;
            return;
        }

        offset = transform.position - target.position;
        offsetMag = offset.magnitude;
        targetPosInTargetSpace = target.transform.InverseTransformDirection(transform.position - target.transform.position);
    }

    /// <summary>
    /// Método que hace la actualización de la posición, mirando la posición del target
    /// y cambiando (suavizando) la posición de la cámara.
    /// </summary>
    void LateUpdate()
    {
        // Posición que querríamos tener
        Vector3 newPos = target.transform.TransformPoint(targetPosInTargetSpace);
        EnsureCanSeeTargetFrom(newPos);

        // Movemos la cámara
        transform.position = Vector3.Lerp(
            transform.position, newPos, Time.deltaTime * smoothLevel);

        // Y hacemos que mire al target
        SmoothLookAt();
    }
    
    void EnsureCanSeeTargetFrom(Vector3 checkPos)
    {
        RaycastHit hit;

        if (Physics.Raycast(checkPos, target.position - checkPos + Vector3.up * 0.3f, out hit, offsetMag))
            // Si no es el target...
            if (hit.transform != target)
            {
                // Lo intentamos hacer transparente
                hit.collider.gameObject.SendMessage("ActivaTransparencia", SendMessageOptions.DontRequireReceiver);
            }
    }

    /// <summary>
    /// Cambia la rotación (con el factor de suavizado) para que se mire
    /// hacia el jugador.
    /// </summary>
    /// (Extraído de un tutorial de Unity.)
    void SmoothLookAt()
    {
        // Create a vector from the camera towards the player.
        Vector3 relPlayerPosition = target.position - transform.position + 0.5f *Vector3.up;

        // Create a rotation based on the relative position of the player being the forward vector.
        Quaternion lookAtRotation = Quaternion.LookRotation(relPlayerPosition, Vector3.up);

        // Lerp the camera's rotation between it's current rotation and the rotation that looks at the player.
        transform.rotation = Quaternion.Lerp(transform.rotation, lookAtRotation, smoothLevel * Time.deltaTime);
    }

}
