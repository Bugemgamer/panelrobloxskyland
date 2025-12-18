export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "METHOD_NOT_ALLOWED" });
  }

  try {
    const { usernames } = req.body;

    if (!Array.isArray(usernames) || usernames.length === 0) {
      return res.status(400).json({ error: "NO_DATA" });
    }

    const results = [];
    let invalid = 0;

    for (const raw of usernames) {
      const username = raw.trim();
      if (!username) continue;

      try {
        // 1. Username -> UserID
        const lookup = await fetch(
          "https://users.roblox.com/v1/usernames/users",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ usernames: [username] })
          }
        ).then(r => r.json());

        if (!lookup.data || lookup.data.length === 0) {
          invalid++;
          continue;
        }

        const userId = lookup.data[0].id;
        const get = url => fetch(url).then(r => r.json());

        // 2. Fetch info akun
        const profile = await get(`https://users.roblox.com/v1/users/${userId}`);
        const friends = await get(`https://friends.roblox.com/v1/users/${userId}/friends/count`);
        const followers = await get(`https://friends.roblox.com/v1/users/${userId}/followers/count`);
        const groups = await get(`https://groups.roblox.com/v1/users/${userId}/groups/roles`);

        results.push({
          username: profile.name,
          userId: userId,
          displayName: profile.displayName,
          age: profile.age,
          created: profile.created.split("T")[0],
          friends: friends.count,
          followers: followers.count,
          groups: groups.data.length,
          banned: profile.isBanned,
          profileUrl: `https://www.roblox.com/users/${userId}/profile`
        });

      } catch (e) {
        invalid++;
        continue;
      }
    }

    return res.json({
      total: usernames.length,
      live: results.length,
      invalid: invalid,
      results: results
    });

  } catch (e) {
    return res.status(500).json({ error: "API_ERROR" });
  }
}