# Start your code below, you can access parameter values as normal list starting from index 1 e.g. i = parameter[1], you can write to output value as normal list starting from index 1 e.g. output[1]= 1+1

obj = parameter[1]["data"]
arrlgt = parameter[1]["count"]["total"] - 1
water = obj[arrlgt]["Depth"]
threshold = 30

if int(water) < threshold:
    msgbody='<p>The current water level '+water+' is below threshold, the reading is less than '+str(threshold)+'.</p><br>'
    output[1]="[Warning] Water Level Reading Below Threshold "
    output[2]=msgbody
    output[3]=2

# end your code here #
