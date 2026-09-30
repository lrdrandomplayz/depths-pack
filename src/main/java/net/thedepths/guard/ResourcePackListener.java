package net.thedepths.guard;

import net.kyori.adventure.text.minimessage.MiniMessage;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerResourcePackStatusEvent;

final class ResourcePackListener implements Listener {

    private final DepthsGuardPlugin plugin;

    ResourcePackListener(DepthsGuardPlugin plugin) {
        this.plugin = plugin;
    }

    @EventHandler
    public void onStatus(PlayerResourcePackStatusEvent event) {
        if (event.getPlayer().hasPermission("depthsguard.bypass")) return;
        String key = switch (event.getStatus()) {
            case DECLINED -> plugin.getConfig().getBoolean("resource-pack.kick-on-decline") ? "decline-message" : null;
            case FAILED_DOWNLOAD, INVALID_URL, FAILED_RELOAD, DISCARDED ->
                    plugin.getConfig().getBoolean("resource-pack.kick-on-fail") ? "fail-message" : null;
            default -> null;
        };
        if (key == null) return;
        String message = plugin.getConfig().getString("resource-pack." + key);
        // Kick next tick: kicking inside the status packet handler can race the configuration phase.
        plugin.getServer().getScheduler().runTask(plugin, () -> {
            if (event.getPlayer().isOnline()) {
                event.getPlayer().kick(MiniMessage.miniMessage().deserialize(message == null ? "" : message));
            }
        });
    }
}
