export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "METHOD_NOT_ALLOWED" });
  }

  try {
    const { username } = req.body;
    if (!username) {
      return res.status(400).json({ error: "NO_USERNAME" });
    }

    // Username -> UserID
    const lookup = await fetch(
      "https://users.roblox.com/v1/usernames/users",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usernames: [username] })
      }
    ).then(r => r.json());

    if (!lookup.data || lookup.data.length === 0) {
      return res.json({ live: false });
    }

    const userId = lookup.data[0].id;
    const get = url => fetch(url).then(r => r.json());

    // Core profile
    const profile = await get(`https://users.roblox.com/v1/users/${userId}`);
    const friends = await get(`https://friends.roblox.com/v1/users/${userId}/friends/count`);
    const followers = await get(`https://friends.roblox.com/v1/users/${userId}/followers/count`);
    const following = await get(`https://friends.roblox.com/v1/users/${userId}/followings/count`);
    const groups = await get(`https://groups.roblox.com/v1/users/${userId}/groups/roles`);
    const badges = await get(`https://badges.roblox.com/v1/users/${userId}/badges?limit=100`);
    const collectibles = await get(`https://inventory.roblox.com/v1/users/${userId}/assets/collectibles?limit=10`);
    const inventoryOpen = await get(`https://inventory.roblox.com/v1/users/${userId}/can-view-inventory`);
    const premium = await fetch(
      `https://premiumfeatures.roblox.com/v1/users/${userId}/validate-membership`
    ).then(r => r.json());

    // Group owner count
    let ownerCount = 0;
    groups.data.forEach(g => {
      if (g.role.rank === 255) ownerCount++;
    });

    return res.json({
      live: true,
      username: profile.name,
      displayName: profile.displayName,
      userId: userId,
      verified: profile.isVerified,
      premium: premium === true,
      age: profile.age,
      created: profile.created.split("T")[0],
      description: profile.description || "",
      descLength: (profile.description || "").length,
      friends: friends.count,
      followers: followers.count,
      following: following.count,
      groups: groups.data.length,
      groupOwner: ownerCount,
      badges: badges.data.length,
      lastBadge: badges.data[0]?.awardedDate?.split("T")[0] || "N/A",
      limited: collectibles.data.length,
      inventoryOpen: inventoryOpen.canView,
      banned: profile.isBanned,
      avatar: `https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds=${userId}&size=150x150&format=Png`,
      profileUrl: `https://www.roblox.com/users/${userId}/profile`
    });

  } catch (e) {
    return res.status(500).json({ error: "API_ERROR" });
  }
}
