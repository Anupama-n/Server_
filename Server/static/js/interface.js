async function fetchVehicleData(actual_number_plate) {
  try {
    const response = await fetch(`/vehicles/${actual_number_plate}`);
    if (!response.ok) {
      throw new Error('Vehicle details not found');
    }
    const vehicleDetails = await response.json();

    const parkingResponse = await fetch(`/parking-slots/${actual_number_plate}`);
    if (!parkingResponse.ok) {
      throw new Error('Parking slots not found');
    }
    const parkingSlots = await parkingResponse.json();

    return { vehicleDetails, parkingSlots };
  } catch (error) {
    console.error('Error fetching data:', error.message);
    return null;
  }
}

// Function to find and display vehicle details and parking slots
async function findDescription() {
  const plateNumber = document.getElementById("plateNumber").value.trim(); 
  const descriptionArea = document.getElementById("descriptionArea");

  if (!plateNumber) {
    descriptionArea.value = "Please enter a valid actual number plate.";
    return;
  }

  const { vehicleDetails, parkingSlots } = await fetchVehicleData(plateNumber);

  if (vehicleDetails && parkingSlots.length > 0) {
    let details = `Vehicle ID: ${vehicleDetails.vehicle_id}\n`;
    details += `Vehicle Type: ${vehicleDetails.vehicle_type}\n`;
    details += `Entry Time: ${vehicleDetails.entry_time}\n`;
    details += `Exit Time: ${vehicleDetails.exit_time || 'Not exited yet'}\n`;
    details += `Parking Fees: ${vehicleDetails.parking_fees}\n\n`;
    
    details += `Parking Slots:\n`;
    parkingSlots.forEach(slot => {
      details += `Slot ID: ${slot.slot_id}, Type: ${slot.slot_type}\n`;
    });

    descriptionArea.value = details;
  } else {
    descriptionArea.value = "Details not available or invalid actual number plate.";
  }
}

// Event listener when DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("findDescriptionButton").addEventListener("click", findDescription);
});
