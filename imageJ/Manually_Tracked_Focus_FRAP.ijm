// set focus width
focus_diameter = 11;
// set spot width
spot_diameter = 19;

//Set Measurements
run("Set Measurements...", "mean redirect=None decimal=3");

//Select "Input" table
selectWindow("Input")

tracks = Table.getColumn("Track n°");
slices = Table.getColumn("Slice n°");
X = Table.getColumn("X");
Y = Table.getColumn("Y");
//Array.print(X);

//Define the max iterations to stop looping as Results table grows
nMax = Table.size();

//Preallocate result arrays
focus_intensities = newArray(nMax);
spot_intensities = newArray(nMax);

// loop through the Results table
for (i=0; i<nMax; i++) {

	// get ROI parameters from Results
	slice = slices[i];
	x = X[i];
	y = Y[i];
	//print(slice);
	
	// make an ROI for each frame
	makeOval(x-(focus_diameter/2), y-(focus_diameter/2), focus_diameter, focus_diameter);
	
	// set slice
	Roi.setPosition(slice);  //Only works before adding to manager
	
	// add focus to Manager
	roiManager("Add");
	roiManager("select", roiManager("count")-1);
	
	// measure focus
	roiManager("measure");
	focus_intensity = getResult("Mean"); //Assuming Mean was measured and is all that is desired

	// save focus values to array 
	focus_intensities[i] = focus_intensity;

	// generate spot ROI
	// outer circle
	makeOval(x-(spot_diameter/2), y-(spot_diameter/2), spot_diameter, spot_diameter);
	Roi.setPosition(slice);
	roiManager("Add");
	roiManager("select", newArray(roiManager("count")-2,roiManager("count")-1));
	roiManager("XOR");

	// add to Manager
	roiManager("Add");
	roiManager("select", roiManager("count")-1);
	
	// measure spot
	roiManager("measure");
	spot_intensity = getResult("Mean"); //Assuming Mean was measured and is all that is desired

	// save focus values to array 
	spot_intensities[i] = spot_intensity;
	
}

Array.show("Results", tracks, slices, X, Y, focus_intensities, spot_intensities)