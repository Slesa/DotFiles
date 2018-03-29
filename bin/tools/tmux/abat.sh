tmux -S ~/.tmux has-session -t abat
if [ $? != 0 ]
then
	tmux -S ~/.tmux new-session -s abat -n cpp -d
	tmux -S ~/.tmux send-keys -t abat 'cd ~abat/Plus_Cpp' C-m

	tmux -S ~/.tmux new-window -n client -t abat
	tmux -S ~/.tmux send-keys -t abat:2 'cd ~abat/Plus_Client' C-m

	tmux -S ~/.tmux new-window -n tools -t abat
	tmux -S ~/.tmux send-keys -t abat:3 'cd ~abat/Plus_Tools' C-m


	tmux -S ~/.tmux split-window -v -t abat:1
	tmux -S ~/.tmux split-window -v -t abat:2
	tmux -S ~/.tmux split-window -v -t abat:3

	tmux -S ~/.tmux select-window -t abat:1
fi
tmux -S ~/.tmux attach -t abat
