package mclib

import (
	"fmt"
	"log"
	"log/slog"
	"net"
	"net/http"
)

func init() {
}

// custom ListenAndServer
type tcpKeepAliveListener struct {
	*net.TCPListener
}

func listenAndServe(addr string, handler http.Handler) error {
	srv := &http.Server{Addr: addr, Handler: handler}
	addr = srv.Addr
	if addr == "" {
		addr = ":http"
	}
	ln, err := net.Listen("tcp4", addr) // IPv4 only
	if err != nil {
		return err
	}
	return srv.Serve(tcpKeepAliveListener{ln.(*net.TCPListener)})
}

var staticDir string = "../static/" // by default, it's static/ folder with same level as src/
var staticDirRegistered = false

func SetStaticDir(dir string) {
	staticDir = dir
}

func StartServer(port int) {
	slog.Info("starting server", "port", port)

	if !staticDirRegistered && staticDir != "" {
		staticDirRegistered = true
		slog.Info("set static dir", "dir", staticDir)
		dir := http.Dir(staticDir)
		handler := http.StripPrefix("/static/", http.FileServer(dir))
		http.Handle("/static/", handler)

		http.HandleFunc("/", defaultHandler)
	}

	err := http.ListenAndServe(fmt.Sprintf(":%d", port), nil)
	if err != nil {
		log.Fatal(err)
	}
}
