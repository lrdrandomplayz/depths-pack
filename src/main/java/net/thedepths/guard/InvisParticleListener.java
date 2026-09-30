package net.thedepths.guard;

import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityPotionEffectEvent;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.potion.PotionEffect;
import org.bukkit.potion.PotionEffectType;

/**
 * Invisibility particles are drawn client-side from the effect list the server sends.
 * Swapping every invisibility effect for a particle-free copy means that list is empty,
 * so packs like Obvious Invisibility Particles or InvisAlert+ have nothing to draw.
 */
final class InvisParticleListener implements Listener {

    @EventHandler(priority = EventPriority.HIGHEST, ignoreCancelled = true)
    public void onEffect(EntityPotionEffectEvent event) {
        if (!(event.getEntity() instanceof Player player)) return;
        if (event.getAction() != EntityPotionEffectEvent.Action.ADDED
                && event.getAction() != EntityPotionEffectEvent.Action.CHANGED) return;
        PotionEffect effect = event.getNewEffect();
        if (effect == null || !effect.getType().equals(PotionEffectType.INVISIBILITY)) return;
        if (!effect.hasParticles()) return;

        // Apply the particle-free copy instead, in the same tick, so no particle
        // data is ever sent. The re-fired event has particles off and is ignored.
        event.setCancelled(true);
        player.addPotionEffect(quiet(effect));
    }

    @EventHandler
    public void onJoin(PlayerJoinEvent event) {
        strip(event.getPlayer());
    }

    void strip(Player player) {
        PotionEffect effect = player.getPotionEffect(PotionEffectType.INVISIBILITY);
        if (effect != null && effect.hasParticles()) {
            player.removePotionEffect(PotionEffectType.INVISIBILITY);
            player.addPotionEffect(quiet(effect));
        }
    }

    private static PotionEffect quiet(PotionEffect effect) {
        return new PotionEffect(effect.getType(), effect.getDuration(), effect.getAmplifier(),
                effect.isAmbient(), false, effect.hasIcon());
    }
}
