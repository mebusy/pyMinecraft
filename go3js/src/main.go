package main

import (
	"go3js/mclib"
	// log "log/slog"
)

func main() {
	// log.Info("hello slog", "key1", 1, "key2", 3)
	mclib.StartServer(7107)
}
