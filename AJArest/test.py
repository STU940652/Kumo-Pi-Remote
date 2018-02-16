import kumo

c = kumo.Client("http://10.70.58.25")

for i in range(1,17):
	name = "%3i: " % (i)
	name += c.getParameter('eParamID_XPT_Destination%i_Line_1' % (i))[1]
	name += ' '
	name += c.getParameter('eParamID_XPT_Destination%i_Line_2' % (i))[1]
	
	source = c.getParameter('eParamID_XPT_Destination%i_Status' % (i))[1]

	sourcename = "%3s: " % (source)
	sourcename += c.getParameter('eParamID_XPT_Source%s_Line_1' % (source))[1]
	sourcename += ' '
	sourcename += c.getParameter('eParamID_XPT_Source%s_Line_2' % (source))[1]

	print("%-15s = %s" % (name, sourcename))

# print c.setParameter('eParamID_XPT_Destination3_Status','9')
