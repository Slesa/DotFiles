tmux has-session -t abat
if [ $? != 0 ]
then
	tmux new-session -s abat -n cpp -d
	tmux send-keys -t abat 'cd ~abat/Plus_Cpp' C-m

	tmux new-window -n client -t abat
	tmux send-keys -t abat:2 'cd ~abat/Plus_Client' C-m

	tmux split-window -v -t abat:1
	tmux split-window -v -t abat:2

	tmux select-window -t abat:1
fi
tmux attach -t abat
