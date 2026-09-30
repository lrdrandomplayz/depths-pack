package net.thedepths.guard;

import org.bukkit.plugin.java.JavaPlugin;

public final class DepthsGuardPlugin extends JavaPlugin {

    @Override
    public void onEnable() {
        saveDefaultConfig();
        if (getConfig().getBoolean("hide-invisibility-particles")) {
            InvisParticleListener invis = new InvisParticleListener();
            getServer().getPluginManager().registerEvents(invis, this);
            getServer().getOnlinePlayers().forEach(invis::strip);
        }
        getServer().getPluginManager().registerEvents(new ResourcePackListener(this), this);
    }
}
