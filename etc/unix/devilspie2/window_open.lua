debug_print("Application: " .. get_application_name())
debug_print("Window: " .. get_window_name())

maxx, maxy = get_screen_geometry()


if string.match(get_application_name(), "cawbird") then
	set_window_workspace(2)
	maximize_vertically()
end

if string.match(get_application_name(), "Pidgin") then
	set_window_workspace(2)
	if string_match(get_window_name(), "NickServ") then
		set_window_position(maxx/2,0)
		maximize_vertically()
	end
end

if string.match(get_application_name(), "Thunderbird") then
	set_window_workspace(2)
	maximize()
end

