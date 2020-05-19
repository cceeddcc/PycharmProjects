import brain

print(brain.doc)
# help(brain)


# read brain
df_edlist, df_know = brain.load_brain()

# modify brain
brain.mod_brain(df_edlist,df_know)

# save_brain()
brain.save_brain()


# visualization
brain.visualize_brain(df_edlist[df_edlist["n1"]=="invertibility"])
