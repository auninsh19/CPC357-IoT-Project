# Start your code below, you can access parameter values as normal list starting from index 1 e.g. i = parameter[1], you can write to output value as normal list starting from index 1 e.g. output[1]= 1+1

obj = parameter[1]["data"]
arrlgt = parameter[1]["count"]["total"] - 1
temp = obj[arrlgt]["Temperature"]
threshold = 35

if int(temp) > threshold or int(temp) == 'None':
    msgbody='<p>The current temperature value '+temp+' is over threshold, the reading is more than '+str(threshold)+'.</p><br>'
    output[1]="[Warning] Temperature Reading over Threshold! "
    output[2]=msgbody
    output[3]=2

# end your code here #
