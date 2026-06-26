using UnityEngine;
using TMPro;
using UnityEngine.InputSystem;

public class HouseCanvasController : MonoBehaviour
{
    [Header("UI Panel")]
    public GameObject uiPanel;

    [Header("Text References")]
    public TextMeshProUGUI titleText;
    public TextMeshProUGUI priceText;
    public TextMeshProUGUI areaText;
    public TextMeshProUGUI descText;
    public TextMeshProUGUI statusText;
    public TextMeshProUGUI residentsText;

    private Camera mainCamera;

    void Start()
    {
        mainCamera = Camera.main;
        if (uiPanel != null)
        {
            uiPanel.SetActive(false);
        }
    }

    void Update()
    {
        if (Mouse.current != null && Mouse.current.leftButton.wasPressedThisFrame)
        {
            HandleClick();
        }
    }

    private void HandleClick()
    {
        if (mainCamera == null) return;

        Vector2 mousePos = Mouse.current.position.ReadValue();
        Ray ray = mainCamera.ScreenPointToRay(mousePos);

        if (Physics.Raycast(ray, out RaycastHit hit))
        {
            GameObject clickedObject = hit.collider.gameObject;

            if (clickedObject.TryGetComponent(out HouseComponent houseComp) && houseComp.Data != null)
            {
                ShowHouseData(houseComp.Data);
                return;
            }
        }

        // If we click nothing or something else, hide the UI
        HideUI();
    }

    private void ShowHouseData(HouseData data)
    {
        if (titleText != null) titleText.text = data.title;
        if (priceText != null) priceText.text = $"Price: {data.price:N0} VND";
        if (areaText != null) areaText.text = $"Area: {data.area_m2} m²";
        if (descText != null) descText.text = $"Description: {data.description}";
        if (statusText != null) statusText.text = $"Status: {data.status}";
        if (residentsText != null) residentsText.text = $"Residents: {data.residential_number}";

        if (uiPanel != null)
        {
            uiPanel.SetActive(true);
        }
    }

    private void HideUI()
    {
        if (uiPanel != null)
        {
            uiPanel.SetActive(false);
        }
    }
}
