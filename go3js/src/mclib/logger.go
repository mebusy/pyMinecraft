package mclib

import ()

import (
	"context"
	"encoding/json"
	"io"
	"log"
	"log/slog"

	// "github.com/fatih/color"
	"os"
)

type PrettyHandlerOptions struct {
	SlogOpts slog.HandlerOptions
}

type PrettyHandler struct {
	slog.Handler
	l *log.Logger
}

func (h *PrettyHandler) Handle(ctx context.Context, r slog.Record) error {
	level := r.Level.String() + ":"

	/*
		switch r.Level {
		case slog.LevelDebug:
			level = color.MagentaString(level)
		case slog.LevelInfo:
			level = color.BlueString(level)
		case slog.LevelWarn:
			level = color.YellowString(level)
		case slog.LevelError:
			level = color.RedString(level)
		}
	*/

	fields := make(map[string]interface{}, r.NumAttrs())
	r.Attrs(func(a slog.Attr) bool {
		fields[a.Key] = a.Value.Any()

		return true
	})

	// b, err := json.MarshalIndent(fields, "", "  ")
	b, err := json.Marshal(fields)
	if err != nil {
		return err
	}

	timeStr := r.Time.Format("[15:05:05.000]")
	// msg := color.CyanString(r.Message)
	// kvPairs := color.WhiteString(string(b))
	msg := r.Message
	kvPairs := string(b)

	h.l.Println(timeStr, level, msg, kvPairs)

	return nil
}

func NewPrettyHandler(
	out io.Writer,
	opts PrettyHandlerOptions,
) *PrettyHandler {
	h := &PrettyHandler{
		Handler: slog.NewJSONHandler(out, &opts.SlogOpts),
		l:       log.New(out, "", 0),
	}

	return h
}

func init() {
	// init slog
	// logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	opts := PrettyHandlerOptions{
		SlogOpts: slog.HandlerOptions{
			Level: slog.LevelDebug,
		},
	}
	handler := NewPrettyHandler(os.Stdout, opts)
	logger := slog.New(handler)
	slog.SetDefault(logger)
}
