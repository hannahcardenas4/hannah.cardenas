#%%
import matplotlib.pyplot as plt 
#%%
plt.plot([50, 50, 100, 200], [183, 130, 346, 100], 'ro')
#plt.plot([50, 100, 200], [130, 115, 100])
plt.axis([0, 250, 0, 400])
plt.xlabel('Exposure Time (ms)')
plt.ylabel('Error Value')
# label = "Actual values"
# label = "Theoretical values"
plt.suptitle('How changing exposure times affects the error values of our CellPose models')
# plt.legend(label)
location = 0 # For the best location
legend_drawn_flag = True
plt.legend(["Generated values", "Expected values"], loc=1, frameon=legend_drawn_flag)
plt.show()
